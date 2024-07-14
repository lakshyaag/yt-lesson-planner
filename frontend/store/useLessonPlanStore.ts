import { create } from "zustand";
import { SearchResponse } from "@/lib/types";

interface LessonPlanState {
  lessonPlan: SearchResponse | null;
  setLessonPlan: (data: SearchResponse) => void;
}

export const useLessonPlanStore = create<LessonPlanState>((set) => ({
  lessonPlan: null,
  setLessonPlan: (data) => set({ lessonPlan: data }),
}));
