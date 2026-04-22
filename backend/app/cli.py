"""Typer CLI for 990 Beacon.

Agent-facing wrapper over the FastAPI backend. Prints JSON to stdout when
``--json`` is set; human-readable text otherwise. Error codes: 0 success,
1 error (auth, network, server), 2 not found.
"""

from __future__ import annotations

import json as _json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, NoReturn

import typer

from app.cli_client import (
    BeaconAuthError,
    BeaconClient,
    BeaconError,
    BeaconNetworkError,
    BeaconNotFoundError,
)

app = typer.Typer(
    help="990 Beacon CLI — agent-facing wrapper over the FastAPI backend.",
    no_args_is_help=True,
    add_completion=False,
)
org_app = typer.Typer(
    help="Organization profile commands.",
    no_args_is_help=True,
    add_completion=False,
)
app.add_typer(org_app, name="org")


@dataclass
class Config:
    base_url: str
    token: str | None
    timeout: float

    def client(self) -> BeaconClient:
        return BeaconClient(
            base_url=self.base_url,
            token=self.token,
            timeout=self.timeout,
        )


@app.callback()
def main(
    ctx: typer.Context,
    base_url: str = typer.Option(
        "http://localhost:8000",
        "--base-url",
        envvar="BEACON_API_URL",
        help="Backend base URL.",
    ),
    token: str | None = typer.Option(
        None,
        "--token",
        envvar="BEACON_API_TOKEN",
        help="Clerk JWT bearer token (copied from the web app).",
    ),
    timeout: float = typer.Option(
        30.0, "--timeout", help="HTTP timeout in seconds."
    ),
) -> None:
    ctx.obj = Config(base_url=base_url, token=token, timeout=timeout)


def _call(
    ctx: typer.Context, as_json: bool, fn: Callable[[BeaconClient], Any]
) -> Any:
    try:
        with ctx.obj.client() as client:
            return fn(client)
    except BeaconNotFoundError as exc:
        _die(str(exc), 2, as_json)
    except BeaconAuthError as exc:
        _die(str(exc) or "authentication failed", 1, as_json)
    except BeaconNetworkError as exc:
        _die(f"network error: {exc}", 1, as_json)
    except BeaconError as exc:
        _die(str(exc), 1, as_json)


def _die(message: str, code: int, as_json: bool) -> NoReturn:
    if as_json:
        typer.echo(_json.dumps({"error": message, "code": code}))
    else:
        typer.echo(message, err=True)
    raise typer.Exit(code=code)


def _emit_json(data: Any) -> None:
    typer.echo(_json.dumps(data, default=str))


@app.command()
def health(
    ctx: typer.Context,
    as_json: bool = typer.Option(
        False, "--json", help="Emit JSON to stdout."
    ),
) -> None:
    """Backend health check (no auth required)."""
    data = _call(ctx, as_json, lambda c: c.get("/health"))
    if as_json:
        _emit_json(data)
    else:
        typer.echo(
            f"status: {data.get('status')}  db: {data.get('db')}  "
            f"version: {data.get('version')}"
        )


@app.command()
def whoami(
    ctx: typer.Context,
    as_json: bool = typer.Option(
        False, "--json", help="Emit JSON to stdout."
    ),
) -> None:
    """Show the authenticated user (doubles as an auth check)."""
    data = _call(ctx, as_json, lambda c: c.get("/api/v1/me"))
    if as_json:
        _emit_json(data)
    else:
        typer.echo(
            f"{data.get('email')}  ({data.get('plan_tier')})  "
            f"id={data.get('id')}"
        )


@app.command()
def search(
    ctx: typer.Context,
    query: str = typer.Argument(..., help="Search query."),
    state: str | None = typer.Option(
        None, "--state", help="Two-letter state code."
    ),
    ntee: str | None = typer.Option(None, "--ntee", help="NTEE code."),
    min_revenue: int | None = typer.Option(None, "--min-revenue"),
    max_revenue: int | None = typer.Option(None, "--max-revenue"),
    min_assets: int | None = typer.Option(None, "--min-assets"),
    max_assets: int | None = typer.Option(None, "--max-assets"),
    filing_year: int | None = typer.Option(None, "--filing-year"),
    page: int = typer.Option(1, "--page", min=1),
    page_size: int = typer.Option(20, "--page-size", min=1, max=100),
    as_json: bool = typer.Option(
        False, "--json", help="Emit JSON to stdout."
    ),
) -> None:
    """Search organizations."""
    params = {
        "q": query,
        "state": state,
        "ntee_code": ntee,
        "min_revenue": min_revenue,
        "max_revenue": max_revenue,
        "min_assets": min_assets,
        "max_assets": max_assets,
        "filing_year": filing_year,
        "page": page,
        "page_size": page_size,
    }
    data = _call(
        ctx, as_json, lambda c: c.get("/api/v1/search", params=params)
    )
    if as_json:
        _emit_json(data)
    else:
        total = data.get("total", 0)
        typer.echo(
            f"{total} result(s), page {data.get('page')}/"
            f"{data.get('total_pages')}"
        )
        for item in data.get("items", []):
            rev = item.get("latest_revenue")
            rev_str = f"${rev:,}" if rev is not None else "—"
            typer.echo(
                f"  {item.get('ein')}  {item.get('name')}  "
                f"[{item.get('state') or '—'}]  {rev_str}"
            )


@app.command()
def typeahead(
    ctx: typer.Context,
    query: str = typer.Argument(..., help="Typeahead query (min length 2)."),
    as_json: bool = typer.Option(
        False, "--json", help="Emit JSON to stdout."
    ),
) -> None:
    """Typeahead name suggestions."""
    data = _call(
        ctx,
        as_json,
        lambda c: c.get("/api/v1/search/typeahead", params={"q": query}),
    )
    if as_json:
        _emit_json(data)
    else:
        for item in data:
            typer.echo(
                f"{item.get('ein')}  {item.get('name')}  "
                f"[{item.get('state') or '—'}]"
            )


@org_app.command("ein")
def org_by_ein(
    ctx: typer.Context,
    ein: str = typer.Argument(..., help="Employer Identification Number."),
    as_json: bool = typer.Option(
        False, "--json", help="Emit JSON to stdout."
    ),
) -> None:
    """Look up an organization profile by EIN."""
    data = _call(
        ctx, as_json, lambda c: c.get(f"/api/v1/organizations/by-ein/{ein}")
    )
    if as_json:
        _emit_json(data)
    else:
        _print_org(data)


@org_app.command("show")
def org_show(
    ctx: typer.Context,
    org_id: str = typer.Argument(..., help="Organization UUID."),
    as_json: bool = typer.Option(
        False, "--json", help="Emit JSON to stdout."
    ),
) -> None:
    """Show an organization profile by UUID."""
    data = _call(
        ctx, as_json, lambda c: c.get(f"/api/v1/organizations/{org_id}")
    )
    if as_json:
        _emit_json(data)
    else:
        _print_org(data)


@app.command()
def usage(
    ctx: typer.Context,
    as_json: bool = typer.Option(
        False, "--json", help="Emit JSON to stdout."
    ),
) -> None:
    """Show usage summary for the authenticated user."""
    data = _call(ctx, as_json, lambda c: c.get("/api/v1/usage/summary"))
    if as_json:
        _emit_json(data)
    else:
        typer.echo(
            f"searches    today: {data.get('searches_today')}  "
            f"month: {data.get('searches_this_month')}"
        )
        typer.echo(
            f"profile views  today: {data.get('profile_views_today')}  "
            f"month: {data.get('profile_views_this_month')}"
        )


def _print_org(data: dict[str, Any]) -> None:
    typer.echo(f"{data.get('name')}  (EIN {data.get('ein')})")
    loc_parts = [p for p in (data.get("city"), data.get("state")) if p]
    typer.echo(f"  location: {', '.join(loc_parts) if loc_parts else '—'}")
    if data.get("ntee_code"):
        typer.echo(f"  ntee: {data['ntee_code']}")
    metrics = data.get("metrics") or {}
    metric_parts: list[str] = []
    per = metrics.get("program_expense_ratio")
    if per is not None:
        metric_parts.append(f"program_expense_ratio={per:.2%}")
    fe = metrics.get("fundraising_efficiency")
    if fe is not None:
        metric_parts.append(f"fundraising_efficiency={fe:.2f}")
    rg = metrics.get("revenue_growth_rate")
    if rg is not None:
        metric_parts.append(f"revenue_growth_rate={rg:.2%}")
    if metric_parts:
        typer.echo(f"  metrics: {', '.join(metric_parts)}")
    filings = data.get("filings") or []
    typer.echo(f"  filings: {len(filings)}")
    for filing in filings[:5]:
        tr = filing.get("total_revenue")
        tr_str = f"${tr:,}" if tr is not None else "—"
        typer.echo(
            f"    {filing.get('tax_year')}  {filing.get('filing_type')}  "
            f"revenue={tr_str}"
        )


if __name__ == "__main__":
    app()
