type AppShellProps = {
  children: React.ReactNode;
};

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="min-h-screen bg-background">
      <div className="grid min-h-screen grid-cols-[16rem_1fr]">
        <aside className="border-r bg-muted/40 px-6 py-5">
          <div className="text-sm font-medium text-muted-foreground">
            Sidebar placeholder
          </div>
        </aside>
        <div className="flex min-w-0 flex-col">
          <header className="flex h-16 items-center border-b px-6">
            <div className="text-sm font-medium text-muted-foreground">
              Header placeholder
            </div>
          </header>
          <main className="min-w-0 flex-1">{children}</main>
        </div>
      </div>
    </div>
  );
}
