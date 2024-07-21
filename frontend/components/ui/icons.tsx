"use client";

import { cn } from "@/lib/utils";

function IconLogo({ className, ...props }: React.ComponentProps<"svg">) {
  return (
    <svg
      fill="currentColor"
      viewBox="0 0 256 256"
      role="img"
      xmlns="http://www.w3.org/2000/svg"
      className={cn("h-4 w-4", className)}
      {...props}
    >
      <circle cx="128" cy="100" r="18" fill="white"></circle>
      <circle cx="102" cy="146" r="18" fill="white"></circle>
      <circle cx="154" cy="146" r="18" fill="white"></circle>
    </svg>
  );
}

export { IconLogo };
