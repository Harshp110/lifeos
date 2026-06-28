import { APP_NAME } from "@lifeos/config";

export default function HomePage() {
  return (
    <section className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-6 py-16">
      <div className="mx-auto max-w-2xl text-center">
        <p className="text-sm font-medium uppercase tracking-wide text-muted-foreground">
          Foundation
        </p>
        <h1 className="mt-4 text-5xl font-semibold tracking-normal text-foreground">
          {APP_NAME}
        </h1>
        <p className="mt-5 text-lg leading-8 text-muted-foreground">
          AI-first personal operating system.
        </p>
      </div>
    </section>
  );
}
