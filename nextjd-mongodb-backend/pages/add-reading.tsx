"use client";

import React, { Fragment, useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { useSession, signIn, signOut } from 'next-auth/react';
import { useRouter } from 'next/router';
import Slider from '@mui/material/Slider';
import { useMapEvents } from 'react-leaflet'; // Import useMapEvents directly
import 'leaflet/dist/leaflet.css';

// Dynamically import react-leaflet components with SSR disabled
const MapContainer = dynamic(() => import('react-leaflet').then((mod) => mod.MapContainer), { ssr: false });
const TileLayer = dynamic(() => import('react-leaflet').then((mod) => mod.TileLayer), { ssr: false });
const Marker = dynamic(() => import('react-leaflet').then((mod) => mod.Marker), { ssr: false });

export default function AddReading() {
  const { data: session } = useSession();
  const router = useRouter();
  const [form, setForm] = useState({ location: { lat: 0, lng: 0 }, value: 50 });

  useEffect(() => {
    console.log('Session from useSession():', session);
  }, [session]);

  // If the user is not logged in, show a message and a login button
  if (!session) {
    return (
      <Fragment>
        <div>
          <p>You need to be authenticated to add readings.</p>
          <button onClick={() => signIn()}>Sign in</button>
        </div>
      </Fragment>
    );
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/add-reading', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.accessToken}`, // Ensure the session token is sent with the request
          credentials: 'include', // This ensures cookies are sent with the request
        },
        body: JSON.stringify({ ...form, userId: session.user.id }),
      });
      if (res.ok) {
        router.push('/');
      } else {
        console.error('Failed to add reading');
      }
    } catch (error) {
      console.error('Error adding reading:', error);
    }
  };

  function LocationMarker() {
    useMapEvents({
      click(e) {
        setForm({ ...form, location: e.latlng });
      },
    });

    return form.location ? (
      <Marker position={form.location}></Marker>
    ) : null;
  }

  return (
    <div className="flex items-center justify-center min-h-screen p-8">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: '400px', width: '100%' }}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          <LocationMarker />
        </MapContainer>
        <Slider
          value={form.value}
          onChange={(e, newValue) => setForm({ ...form, value: newValue })}
          aria-labelledby="continuous-slider"
          valueLabelDisplay="auto"
          min={0}
          max={100}
        />
        <button type="submit">Add Reading</button>
        <button type="button" onClick={() => signOut()}>Logout</button>
      </form>
    </div>
  );
}