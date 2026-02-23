import { vi } from "vitest";

// Mock @clerk/nextjs
export const mockClerk = {
  useUser: vi.fn(() => ({
    isSignedIn: true,
    user: {
      id: "user_test123",
      firstName: "Test",
      lastName: "User",
      emailAddresses: [{ emailAddress: "test@example.com" }],
    },
    isLoaded: true,
  })),
  useAuth: vi.fn(() => ({
    isSignedIn: true,
    getToken: vi.fn().mockResolvedValue("mock-token"),
    isLoaded: true,
  })),
  useClerk: vi.fn(() => ({
    signOut: vi.fn(),
  })),
  ClerkProvider: ({ children }: { children: React.ReactNode }) => (
    <>{children}</>
  ),
  SignIn: () => <div data-testid="clerk-sign-in">Sign In</div>,
  SignUp: () => <div data-testid="clerk-sign-up">Sign Up</div>,
  UserButton: () => <div data-testid="clerk-user-button">User Button</div>,
  SignedIn: ({ children }: { children: React.ReactNode }) => <>{children}</>,
  SignedOut: ({ children }: { children: React.ReactNode }) => <>{children}</>,
};

vi.mock("@clerk/nextjs", () => mockClerk);

// Mock @clerk/nextjs/server
vi.mock("@clerk/nextjs/server", () => ({
  clerkMiddleware: vi.fn(() => vi.fn()),
  createRouteMatcher: vi.fn(() => vi.fn(() => false)),
  auth: vi.fn().mockResolvedValue({ userId: "user_test123" }),
}));
