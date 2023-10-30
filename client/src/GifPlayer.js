// GifPlayer.js
import React from 'react';
import localGif from './images/aud.gif'; 

function GifPlayer({ isPlaying }) {
  return (
    <div className={`gif-container ${isPlaying ? 'visible' : 'hidden'}`}>
      <img src={localGif} alt="Audio Animation" className="audio-gif" />
    </div>
  );
}

export default GifPlayer;
