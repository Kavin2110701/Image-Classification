import React, { useState, useEffect, useRef } from 'react';
import { Button, Upload, Spin, Alert, Layout, Menu } from 'antd';
import { UploadOutlined, InboxOutlined, HomeOutlined, InfoCircleOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import 'antd/dist/reset.css';
import './App.css';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

const { Dragger } = Upload;
const { Header, Content, Footer } = Layout;

function Home() {
  return (
    <div className="home-content">
      <div className="hero">

        <h1>Gold Ornament Image Classification</h1>
        <br></br>
        <h3>Welcome to our project on image classification of gold ornaments. This project aims to accurately identify and classify various components in gold ornament images, such as stones, beads, and tassels.</h3>
        <br></br>
      </div>

     
      <div className="project-overview">
        <h2>Project Overview</h2>
        <br></br>
        <ul>
          <li>Initial attempts with SVM and HOG feature extraction for image partitioning and classification.</li>
          <li>Fine-tuning a six-class classification model for different types of gold chains with various components.</li>
          <li>Adopting a CNN approach for better accuracy in predicting probabilities of components in the images.</li>
          <li>Transitioning to YOLOv8 model with bounding boxes created using RoboFlow, leading to 21 versions with continuous feedback and iterations.</li>
          <li>Finalizing the use of heterogeneous images for realistic predictions and creating separate YOLOv8 models for stones, beads, and tassels.</li>
        </ul>
        <br></br>
        <p>We are currently exploring the RCNN approach to further enhance our model's performance.</p>
      </div>
    </div>
  );
}

function About() {
  return (
    <div className="about-content">
      <h1>About This Project</h1>
      <br></br>
      <p>This project is developed by a team of dedicated students under the guidance of our faculty coordinator. We aim to provide a robust and generic model for classifying gold ornament images by detecting stones, beads, and tassels accurately.</p>
      <br></br>
      <h2>Technologies Used</h2>
      <br></br>
      <ul>
        <li>Machine Learning: SVM, HOG features extraction</li>
        <li>Deep Learning: CNN, YOLOv8</li>
        <li>Tools: RoboFlow for bounding box creation</li>
      </ul>
      <br></br>
      <h2>Future Work</h2>
      <br></br>
      <p>We are working towards incorporating the RCNN approach to enhance our model's accuracy and make it more robust for real-time applications.</p>
    </div>
  );
}
function UploadSection() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [originalImage, setOriginalImage] = useState(null);
  const [predictedImage, setPredictedImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (info) => {
    setSelectedFile(info.file);
  };
  const fetchImageWithHeaders = async (url, setImageCallback) => {
    try {
      const response = await fetch(url, {
        headers: {
          "ngrok-skip-browser-warning": "any",
        },
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      const blob = await response.blob();
      const imageObjectURL = URL.createObjectURL(blob);
      setImageCallback(imageObjectURL);
    } catch (error) {
      console.error('Error fetching image:', error);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    setIsLoading(true);

    if (!selectedFile) {
      setError('No file selected.');
      setIsLoading(false);
      return;
    }

    const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const response = await fetch('https://dd12-2401-4900-4ddd-5d7b-a081-c59b-47d0-cf99.ngrok-free.app/upload/', {
      method: 'POST',
      body: formData,
      headers: new Headers({
        "ngrok-skip-browser-warning": "any",
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Response data:', data); // Log the entire response

    const originalImageURL = `https://dd12-2401-4900-4ddd-5d7b-a081-c59b-47d0-cf99.ngrok-free.app/upload/${data.predicted_image_url}`;
    const predictedImageURL = `https://dd12-2401-4900-4ddd-5d7b-a081-c59b-47d0-cf99.ngrok-free.app/predict/${data.predicted_image_url}`;

    console.log('Original Image URL:', originalImageURL);
    console.log('Predicted Image URL:', predictedImageURL);

    await fetchImageWithHeaders(originalImageURL, setOriginalImage);
    await fetchImageWithHeaders(predictedImageURL, setPredictedImage);

    console.log('Original Image:', originalImage);
    console.log('Predicted Image:', predictedImage);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="upload-content">
      <h1>Upload</h1>
      <form onSubmit={handleSubmit} className="upload-form">
        <Dragger
          beforeUpload={() => false} // Prevent automatic upload
          onChange={handleFileChange}
          showUploadList={false}
          style={{ padding: '20px' }}
        >
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">Click or drag file to this area to upload</p>
          <p className="ant-upload-hint">Support for a single upload.</p>
        </Dragger>
        <Button type="primary" htmlType="submit" style={{ marginTop: '20px', width: '120px' }}>
          Predict
        </Button>
      </form>
      {error && <Alert message="Error" description={error} type="error" showIcon style={{ marginTop: '20px' }} />}
      {isLoading && (
        <div className="spinner-container">
          <Spin tip="Loading..." />
        </div>
      )}
      <div className="image-container">
        <div className="image-wrapper">
          {originalImage && (
            <motion.div
              initial={{ opacity: 0, y: -50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              style={{ marginTop: '20px' }}
            >
              <h3>Original Image:</h3>
              <img src={originalImage} alt="Original" className="large-image" />
            </motion.div>
          )}
        </div>
        <div className="image-wrapper">
          {predictedImage && (
            <motion.div
              initial={{ opacity: 0, y: -50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              style={{ marginTop: '20px' }}
            >
              <h3>Predicted Image:</h3>
              <img src={predictedImage} alt="Predicted" className="large-image" />
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}

const LiveVideoViewer = () => {
  const [error, setError] = useState(null);
  const [stream, setStream] = useState(null);
  const videoRef = useRef();
  const navigate = useNavigate(); // Create useNavigate instance

  useEffect(() => {
    const getCameraStream = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        setStream(stream);
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        setError('Failed to access camera: ' + err.message);
      }
    };

    getCameraStream();

    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const handleCloseCamera = () => {
    console.log('Closing camera');
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    navigate('/');
    window.location.reload(); // Navigate to home page after closing camera
  };

  return (
    <div className="live-video-viewer">
      <h1>Live Video Feed</h1>
      {stream && <button onClick={handleCloseCamera}>Close Camera</button>}
      <video autoPlay ref={videoRef}></video>
      {error && <div>Error: {error}</div>}
    </div>
  );
};

const menuItems = [
  { label: <Link to="/"><HomeOutlined /> Home</Link>, key: '1' },
  { label: <Link to="/upload"><UploadOutlined /> Upload</Link>, key: '2' },
  { label: <Link to="/about"><InfoCircleOutlined /> About</Link>, key: '3' }
];

function App() {
  return (
    <Router>
      <Layout className="layout">
        <Header>
          <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']} items={menuItems} />
        </Header>
        <Content style={{ padding: '0 50px', overflowY: 'auto' }}>
          <div className="site-layout-content">
            <Routes>
              <Route exact path="/" element={<Home />} />
              <Route path="/upload" element={<UploadSection />} />
              <Route path="/about" element={<About />} />
            </Routes>
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>Gold Ornament Image Classification ©2024 Created by Your Team</Footer>
      </Layout>
    </Router>
  );
}

export default App;
