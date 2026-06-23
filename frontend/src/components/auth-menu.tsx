import { useState } from "react";
import { LogIn, LogOut, UserPlus } from "lucide-react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { fetchCurrentUser, hasStoredSession, login, logout, register } from "@/services/api";

type AuthMode = "login" | "register";

export function AuthMenu() {
  const [open, setOpen] = useState(false);
  const [mode, setMode] = useState<AuthMode>("login");
  const queryClient = useQueryClient();
  const userQuery = useQuery({
    queryKey: ["auth-user"],
    queryFn: fetchCurrentUser,
    enabled: hasStoredSession(),
    retry: false,
  });

  const user = userQuery.data;
  const initials = user?.full_name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  function handleLogout() {
    logout();
    queryClient.setQueryData(["auth-user"], null);
    queryClient.invalidateQueries({ queryKey: ["portfolio"] });
    queryClient.invalidateQueries({ queryKey: ["portfolio-overview"] });
  }

  if (user) {
    return (
      <div className="flex items-center gap-2">
        <div className="hidden sm:flex flex-col items-end leading-tight">
          <span className="text-xs font-medium">{user.full_name}</span>
          <span className="text-[10px] text-muted-foreground">@{user.username}</span>
        </div>
        <Avatar className="h-8 w-8">
          <AvatarFallback>{initials || user.username[0]?.toUpperCase()}</AvatarFallback>
        </Avatar>
        <Button variant="ghost" size="icon" onClick={handleLogout} title="Log out">
          <LogOut className="h-4 w-4" />
        </Button>
      </div>
    );
  }

  return (
    <>
      <Button size="sm" onClick={() => setOpen(true)}>
        <LogIn className="h-4 w-4" />
        Sign in
      </Button>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Account</DialogTitle>
            <DialogDescription>
              Sign in to save portfolio data to your FastAPI account.
            </DialogDescription>
          </DialogHeader>
          <Tabs value={mode} onValueChange={(value) => setMode(value as AuthMode)}>
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="login">Sign in</TabsTrigger>
              <TabsTrigger value="register">Create</TabsTrigger>
            </TabsList>
            <TabsContent value="login" className="mt-4">
              <LoginForm
                onSuccess={() => {
                  setOpen(false);
                  queryClient.invalidateQueries({ queryKey: ["auth-user"] });
                  queryClient.invalidateQueries({ queryKey: ["portfolio"] });
                }}
              />
            </TabsContent>
            <TabsContent value="register" className="mt-4">
              <RegisterForm
                onSuccess={() => {
                  setMode("login");
                }}
              />
            </TabsContent>
          </Tabs>
        </DialogContent>
      </Dialog>
    </>
  );
}

function LoginForm({ onSuccess }: { onSuccess: () => void }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);
    try {
      await login(username, password);
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not sign in");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <Input
        value={username}
        onChange={(event) => setUsername(event.target.value)}
        placeholder="Username"
        autoComplete="username"
        required
      />
      <Input
        value={password}
        onChange={(event) => setPassword(event.target.value)}
        placeholder="Password"
        type="password"
        autoComplete="current-password"
        required
      />
      {error && <p className="text-xs text-destructive">{error}</p>}
      <Button type="submit" className="w-full" isLoading={isSubmitting}>
        <LogIn className="h-4 w-4" />
        Sign in
      </Button>
    </form>
  );
}

function RegisterForm({ onSuccess }: { onSuccess: () => void }) {
  const [form, setForm] = useState({
    username: "",
    email: "",
    full_name: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function update(field: keyof typeof form, value: string) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    setNotice("");
    setIsSubmitting(true);
    try {
      await register(form);
      setNotice("Account created. You can sign in now.");
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not create account");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <Input
        value={form.full_name}
        onChange={(event) => update("full_name", event.target.value)}
        placeholder="Full name"
        autoComplete="name"
        required
      />
      <Input
        value={form.username}
        onChange={(event) => update("username", event.target.value)}
        placeholder="Username"
        autoComplete="username"
        required
      />
      <Input
        value={form.email}
        onChange={(event) => update("email", event.target.value)}
        placeholder="Email"
        type="email"
        autoComplete="email"
        required
      />
      <Input
        value={form.password}
        onChange={(event) => update("password", event.target.value)}
        placeholder="Password"
        type="password"
        autoComplete="new-password"
        required
      />
      {error && <p className="text-xs text-destructive">{error}</p>}
      {notice && <p className="text-xs text-success">{notice}</p>}
      <Button type="submit" className="w-full" isLoading={isSubmitting}>
        <UserPlus className="h-4 w-4" />
        Create account
      </Button>
    </form>
  );
}
