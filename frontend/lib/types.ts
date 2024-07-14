export interface Video {
  video_id: string;
  title: string;
  description: string;
  published_at: string;
  channel_title: string;
  chunk_time_limit: number;
}

export interface Topic {
  objective: string;
  videos: string[];
  description: string;
  steps: string[];
  suggested_activities: string[];
}

export interface LessonPlan {
  title: string;
  topics: Topic[];
  comments: string;
}

export interface SearchResponse {
  original_query: {
    user_input: string;
  };
  learning_objectives: {
    objectives: { index: number; objective: string }[];
  };
  videos: Record<string, Video>;
  lesson_plan: LessonPlan;
}
