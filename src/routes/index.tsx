import { createFileRoute } from "@tanstack/react-router";
import { LastWard } from "@/components/LastWard";

export const Route = createFileRoute("/")({ component: Home });

function Home() {
  return <LastWard />;
}
