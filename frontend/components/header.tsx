import React from "react";
import { ModeToggle } from "./mode-toggle";
import { IconLogo } from "./ui/icons";
import { cn } from "@/lib/utils";

export const Header: React.FC = async () => {
  return (
    <header className="fixed w-full p-1 md:p-2 flex justify-between items-center z-10 backdrop-blur md:backdrop-blur-none bg-background/80 md:bg-transparent">
      <div>
        <a href="/">
          <div className="flex items-center mx-4">
            <IconLogo className={cn("w-5 h-5 mr-2")} />
            <span className="text-lg font-bold">Video YouNiversity</span>
          </div>
        </a>
      </div>
      <div className="flex gap-0.5">
        <ModeToggle />
      </div>
    </header>
  );
};

export default Header;
