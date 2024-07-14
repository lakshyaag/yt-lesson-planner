import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Video, Topic as TopicType } from "@/lib/types";

interface TopicProps {
  topic: TopicType;
  videos: Record<string, Video>;
}

const Topic: React.FC<TopicProps> = ({ topic, videos }) => {
  return (
    <div className="mt-8 p-6 border rounded-lg shadow-sm bg-white">
      <h3 className="text-2xl font-semibold">{topic.description}</h3>
      <div className="mt-6">
        <Tabs defaultValue={topic.videos[0]}>
          <TabsList className="flex space-x-2 mb-4 w-full">
            {topic.videos.map((videoId, index) => (
              <TabsTrigger
                key={videoId}
                value={videoId}
                className="flex-1 px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 text-center"
              >
                {`Video ${index + 1}`}
              </TabsTrigger>
            ))}
          </TabsList>
          {topic.videos.map((videoId, index) => (
            <TabsContent key={videoId} value={videoId} className="p-4">
              <div className="mt-4 p-4 border rounded-lg shadow-sm bg-gray-50">
                <iframe
                  width="100%"
                  height="300"
                  src={`https://www.youtube.com/embed/${videoId}`}
                  title={`Video ${index + 1}`}
                  allowFullScreen
                ></iframe>
                <div className="mt-4">
                  <p className="mt-2 text-gray-700 font-bold">
                    {videos[videoId].title} - {videos[videoId].channel_title}
                  </p>
                </div>
              </div>
            </TabsContent>
          ))}
        </Tabs>
      </div>
      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h4 className="font-semibold">Steps:</h4>
          <ul className="list-disc list-inside">
            {topic.steps.map((step, stepIndex) => (
              <li key={stepIndex} className="mt-2 text-gray-700">
                {step}
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h4 className="font-semibold">Suggested Activities:</h4>
          <ul className="list-disc list-inside">
            {topic.suggested_activities.map((activity, activityIndex) => (
              <li key={activityIndex} className="mt-2 text-gray-700">
                {activity}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Topic;
