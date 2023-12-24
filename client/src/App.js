import { useState, useRef } from 'react';
import axios from 'axios';
import { useReactMediaRecorder } from "react-media-recorder";
import './App.css';
import GifPlayer from './GifPlayer.js';

export default function App() {
  const {
    status,
    startRecording,
    stopRecording,
    mediaBlobUrl,
  } = useReactMediaRecorder({ audio: true });

  const [isRecording, setIsRecording] = useState(false);
  const [audioResponse, setAudioResponse] = useState('');
  const gifPath = 'images/aud.gif';
  const audioRef = useRef();


  // Declare speechHandler and msg variables
  const speechHandler = (msg) => {
    msg.text = audioResponse ? audioResponse : "Response is not received, Sorry";
    window.speechSynthesis.speak(msg);
  };

  const msg = new SpeechSynthesisUtterance();


  const playAudio = () => {
    if (audioResponse) {
      audioRef.current.src = audioResponse;
      audioRef.current.load();
      audioRef.current.play();
    }
  };

  const toggleRecording = async () => {
    if (isRecording && status === "recording") {
      // Stop recording and send to the backend
      stopRecording();
      const response = await fetch(mediaBlobUrl);
      const audioData = await response.blob();
      // await new Promise((resolve) => {
      //   setTimeout(() => {
      //     resolve();
      //   }, 1000); // Adjust the timeout as needed
      // });
      if (status === "stopped" && mediaBlobUrl) {
        await testAsyncCode()
        sendAudioToBackend();
        playAudio();
      }
    } else {
      // Start recording
      startRecording();
    }
    setIsRecording((prevIsRecording) => !prevIsRecording);
  };

  async function testAsyncCode() {
    console.log('Start');
    await new Promise((resolve) => {
      setTimeout(() => {
        resolve();
      }, 2000); // Adjust the timeout as needed
    });
    console.log('End');
  }

  const sendAudioToBackend = async () => {
    try {
      if (!mediaBlobUrl) {
        console.error('mediaBlobUrl is undefined');
        return;
      }
      const response = await fetch(mediaBlobUrl);
      const audioData = await response.blob();

      // Send audioData to the backend
      const formData = new FormData();
      formData.append('file', audioData);
  
      axios.post('http://127.0.0.1:5000/upload_audio/allow-cors', formData, { timeout: 5000 })
        .then((res) => {
          console.log("Response from backend:", res.data.data);
          setAudioResponse(res.data.data);
        })
        .then(() => {
          speechHandler(msg);
          console.log("Speech");
          setIsRecording(false);
        })
        .catch((error) => {
          console.error("Error in axios post:", error);
        });
    } catch (error) {
      console.error("Error in try-catch:", error);
    }
  };

  return (
    <div className="container">
      <h1>Audio CHATBOT</h1>
      {audioResponse && <audio ref={audioRef} controls />}
      <div>
        <p>{status}</p>
        <div>
          {GifPlayer && <img src={gifPath} alt="GIF" />}
        </div>
        <button onClick={toggleRecording}>
          {isRecording ? 'Stop and Send' : 'Start Recording'}
        </button>
      </div>
    </div>
  );
}
