import { useLessonPlanStore } from "@/store/useLessonPlanStore";
import Topic from "@/components/lesson-topic";
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "@/components/ui/accordion";

const LessonPlanDisplay = () => {
  const lessonPlan = useLessonPlanStore((state) => state.lessonPlan);

  if (!lessonPlan) {
    return null;
  }

  return (
    <div className="mt-8 w-full max-w-xl md:max-w-2xl lg:max-w-4xl p-4 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold">{lessonPlan.lesson_plan.title}</h2>
      <p className="mt-4">{lessonPlan.lesson_plan.comments}</p>
      <Accordion type="single" collapsible>
        {lessonPlan.lesson_plan.topics.map((topic, index) => (
          <AccordionItem key={index} value={`item-${index}`}>
            <AccordionTrigger className="text-md text-left">
              {topic.objective}
            </AccordionTrigger>
            <AccordionContent>
              <Topic topic={topic} videos={lessonPlan.videos} />
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </div>
  );
};

export default LessonPlanDisplay;
