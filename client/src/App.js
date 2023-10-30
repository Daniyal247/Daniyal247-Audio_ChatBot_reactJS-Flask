import { useState, useRef } from 'react';
import { useEffect } from 'react';
import { useReactMediaRecorder } from "react-media-recorder";
import './App.css';
import GifPlayer from './GifPlayer';

export default function App() {
  const {
    status,
    startRecording,
    stopRecording,
    mediaBlobUrl,
  } = useReactMediaRecorder({ audio: true });

  const [isRecording, setIsRecording] = useState(false);
  const [showGif, setShowGif] = useState(false);
  const [replyAudioUrl, setReplyAudioUrl] = useState('');
  const gifPAth = 'images/recording.gif';
  const audioRef = useRef();

  const playAudio = () => {
    console.log('playAudio called')
    if (replyAudioUrl) {
      audioRef.current.src = replyAudioUrl;
      audioRef.current.load();
      audioRef.current.play();
    }
  };

  const toggleRecording = () => {
    if (isRecording) {
      // Stop recording and send to the backend
      stopRecording();
      sendAudioToBackend();
    } else {
      // Start recording
      startRecording();
      setShowGif(true);
    }
    setIsRecording((prevIsRecording) => !prevIsRecording);
  };

  const sendAudioToBackend = async () => {
    const response = await fetch(mediaBlobUrl);
    const audioData = await response.blob();
    // Send audioData to the backend
    let formData = new FormData();
    formData.append('file', audioData, 'recorded_audio.mp3');

    fetch('http://localhost:5000/upload_audio', {
      method: 'POST',
      body: formData,
      mode: 'no-cors',
      credentials: 'include'
    })
    .then(response => response.blob())
    .then(data => {
      const audioUrl = URL.createObjectURL(data);
      setReplyAudioUrl(audioUrl);
      console.log(replyAudioUrl)
      playAudio();
    })
    .catch(error => console.error(error));
    setIsRecording(false);
  };

  return (
    <div className="container">
      <h1>Audio CHATBOT</h1>
      <audio src={mediaBlobUrl} controls/>
      <audio ref={audioRef} controls /> {/* Audio element to play the reply */}
      <div>
        <p>{status}</p>
        <div>
          {/* Display the GIF continuously while recording is active */}
          {GifPlayer && <img src={gifPAth} />}
        </div>
        <button onClick={toggleRecording}>
          {isRecording ? 'Stop and Send' : 'Start Recording'}
        </button>
      </div>
    </div>
  );
}
