"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useLessonPlanStore } from "@/store/useLessonPlanStore";
import { useLoadingStore } from "@/store/useLoadingStore";
import Spinner from "@/components/spinner";

const SearchForm = () => {
  const [query, setQuery] = useState("");
  const setLessonPlan = useLessonPlanStore((state) => state.setLessonPlan);
  const setLoading = useLoadingStore((state) => state.setLoading);
  const loading = useLoadingStore((state) => state.loading);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    try {
      const response = await fetch("/api/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      setLessonPlan(data);
    } catch (error) {
      console.error("Error during search:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col items-center">
      <Input
        type="text"
        placeholder="Search for a lesson..."
        className="w-full mb-4"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <Button type="submit" className="w-full" disabled={loading}>
        {loading ? (
          <div className="flex items-center justify-center">
            <Spinner />
            <span className="ml-2">Searching...</span>
          </div>
        ) : (
          "Search"
        )}
      </Button>
    </form>
  );
};

export default SearchForm;
