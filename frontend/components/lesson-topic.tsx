import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Video, Topic as TopicType } from "@/lib/types";

interface TopicProps {
  topic: TopicType;
  videos: Record<string, Video>;
}

const Topic: React.FC<TopicProps> = ({ topic, videos }) => {
  return (
    <div className="mt-8 p-6 border rounded-lg shadow-sm">
      <h3 className="text-lg lg:text-xl font-semibold">{topic.description}</h3>
      <div className="mt-6">
        <Tabs
          defaultValue={`${topic.videos[0].id}-${topic.videos[0].start_timestamp}`}
        >
          <TabsList className="flex space-x-2 mb-4 w-full">
            {topic.videos.map((video, index) => (
              <TabsTrigger
                key={`${video.id}-${video.start_timestamp}`}
                value={`${video.id}-${video.start_timestamp}`}
                className="flex-1 px-4 py-2 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 text-center"
              >
                {`Video ${index + 1}`}
              </TabsTrigger>
            ))}
          </TabsList>

          {topic.videos.map((video, index) => (
            <TabsContent
              key={`${video.id}-${video.start_timestamp}`}
              value={`${video.id}-${video.start_timestamp}`}
              className="p-4"
            >
              <div className="mt-4 p-4 border rounded-lg shadow-sm">
                <iframe
                  width="100%"
                  height="300"
                  src={`https://www.youtube.com/embed/${video.id}?start=${video.start_timestamp}`}
                  title={`Video ${index + 1} (${video.start_timestamp})`}
                  allowFullScreen
                ></iframe>
                <div className="mt-4 p-4 rounded-lg bg-slate-200 dark:bg-slate-800">
                  <p className="text-sm">
                    Title:{" "}
                    <span className="font-semibold">
                      {videos[video.id].title}
                    </span>
                  </p>
                  <p className="text-sm mt-2">
                    Channel:{" "}
                    <span className="font-semibold">
                      {videos[video.id].channel_title}
                    </span>
                  </p>
                  <p className="text-sm mt-2">
                    Timestamp:{" "}
                    <span className="font-semibold">
                      {new Date(video.start_timestamp * 1000)
                        .toISOString()
                        .slice(11, 19)}{" "}
                      to{" "}
                      {new Date(video.end_timestamp * 1000)
                        .toISOString()
                        .slice(11, 19)}
                    </span>
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
              <li key={stepIndex} className="mt-2">
                {step}
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h4 className="font-semibold">Suggested Activities:</h4>
          <ul className="list-disc list-inside">
            {topic.suggested_activities.map((activity, activityIndex) => (
              <li key={activityIndex} className="mt-2">
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
