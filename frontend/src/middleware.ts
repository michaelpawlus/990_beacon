import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const clerkEnabled = !!process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY?.startsWith("pk_");

async function clerkMiddlewareHandler(req: NextRequest) {
  const { clerkMiddleware, createRouteMatcher } = await import("@clerk/nextjs/server");
  const isProtectedRoute = createRouteMatcher(["/dashboard(.*)"]);

  return new Promise<NextResponse>((resolve) => {
    const handler = clerkMiddleware(async (auth, r) => {
      if (isProtectedRoute(r)) {
        await auth.protect();
      }
    });
    resolve(handler(req, {} as any) as any);
  });
}

export default async function middleware(req: NextRequest) {
  if (!clerkEnabled) {
    return NextResponse.next();
  }
  return clerkMiddlewareHandler(req);
}

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
};
