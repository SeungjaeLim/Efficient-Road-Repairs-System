import React, { useState, useEffect } from "react";
import axios from "axios";
import 'leaflet/dist/leaflet.css';
import { Grid } from "@mui/material";
import CardView from "./components/CardView";
import ModalView from "./components/ModalView";

const App = () => {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [open, setOpen] = useState(false);
  
  useEffect(() => {
    axios
      .get("http://localhost:8090/epcis/v2/events", {
        headers: {
          "Content-Type": "application/json",
          "GS1-EPCIS-Version": "2.0.0",
          "GS1-CBV-Version": "2.0.0",
        },
      })
      .then((response) => {
        const eventList = response.data?.epcisBody?.queryResults?.resultBody?.eventList || [];
  
        const cleanedData = eventList.map((event) => ({
          eventTime: event.eventTime || "N/A",
          geoLocation: event.readPoint?.id || "Unknown",
          damageType: event.ilmd?.["https://yourdomain.com/damageType"] || "Unknown",
          repairCost: event.ilmd?.["https://yourdomain.com/repairCost"]?.TotalCost || 0,
          repairItems: event.ilmd?.["https://yourdomain.com/repairCost"]?.items || [],
          dimensions: event.ilmd?.["https://yourdomain.com/dimensions"] || { Width: "N/A", Height: "N/A" },
          image: event.ilmd?.["https://yourdomain.com/filename"]
            ? `http://localhost:5000/static/images/${event.ilmd["https://yourdomain.com/filename"]}`
            : "https://via.placeholder.com/300", // 기본 이미지
        }));
  
        console.log("Cleaned Data with Image Paths:", cleanedData);
        setEvents(cleanedData);
      })
      .catch((error) => {
        console.error("Error Fetching Data:", error);
        setEvents([]);
      });
  }, []);
  
  
  
  
  

  // 모달 열기
  const handleOpen = (event) => {
    setSelectedEvent(event);
    setOpen(true);
  };

  // 모달 닫기
  const handleClose = () => {
    setSelectedEvent(null);
    setOpen(false);
  };

  return (
    <div style={{ padding: 16 }}>
      <Grid container spacing={2}>
        {events.map((event, index) => (
          <Grid item key={index}>
            <CardView data={event} onOpen={handleOpen} />
          </Grid>
        ))}
      </Grid>
      <ModalView open={open} handleClose={handleClose} data={selectedEvent} />
    </div>
  );
};

export default App;
