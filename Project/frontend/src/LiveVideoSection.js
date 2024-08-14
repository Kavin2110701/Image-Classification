// Inside the LiveVideoSection.js file

import React, { useState, useEffect } from 'react';
import { Spin, Alert } from 'antd';

function LiveVideoSection() {
  const [videoFeed, setVideoFeed] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchVideoFeed = async () => {
      setIsLoading(true);
      try {
        const response = await fetch('http://localhost:8000/video_feed');
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        setVideoFeed(URL.createObjectURL(await response.blob()));
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchVideoFeed();

    return () => {
      if (videoFeed) {
        URL.revokeObjectURL(videoFeed);
      }
    };
  }, []);

  return (
    <div className="live-video-content">
      <h1>Live Video Feed</h1>
      {error && <Alert message="Error" description={error} type="error" showIcon style={{ marginTop: '20px' }} />}
      {isLoading && (
        <div className="spinner-container">
          <Spin tip="Loading..." />
        </div>
      )}
      {videoFeed && (
        <video src={videoFeed} autoPlay className="live-video" />
      )}
    </div>
  );
}

export default LiveVideoSection;
