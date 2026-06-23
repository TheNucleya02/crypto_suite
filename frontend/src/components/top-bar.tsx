import { Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";
import { AuthMenu } from "@/components/auth-menu";

interface TopBarProps {
  onMenu: () => void;
  title: string;
}

export function TopBar({ onMenu, title }: TopBarProps) {
  return (
    <header className="sticky top-0 z-30 flex h-16 items-center gap-3 border-b border-border bg-background/80 backdrop-blur-xl px-4 md:px-6">
      <Button
        variant="ghost"
        size="icon"
        className="lg:hidden text-muted-foreground"
        onClick={onMenu}
      >
        <Menu className="h-5 w-5" />
      </Button>
      <div className="flex-1 min-w-0">
        <h1 className="text-base md:text-lg font-semibold tracking-tight truncate">{title}</h1>
      </div>
      <AuthMenu />
      <ThemeToggle />
    </header>
  );
}
