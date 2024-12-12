import React from "react";
import { Card, CardContent, CardMedia, Typography, Button, Box } from "@mui/material";

const CardView = ({ data, onOpen }) => {
  // Geo Location 파싱
  const geoLocation = data.geoLocation || "urn:epc:id:geo:37.7750,-122.4195";
  const coordinates = geoLocation.split(":").pop().split(",");
  const latitude = parseFloat(coordinates[0]).toFixed(3); // 소수점 3자리로 고정
  const longitude = parseFloat(coordinates[1]).toFixed(3);

  return (
    <Card
      style={{
        margin: 8,
        maxWidth: 340,
        borderRadius: 12,
        boxShadow: "0 2px 8px rgba(0, 0, 0, 0.1)",
        overflow: "hidden",
      }}
    >
      {/* 이미지 크기 조정 */}
      <CardMedia
        component="img"
        style={{
          height: 200, // 원하는 이미지 높이
          objectFit: "cover", // 이미지 비율 유지하며 카드에 맞게 채움
        }}
        image={data.image}
        alt="Event Image"
      />
      <CardContent style={{ padding: 12 }}>
        <Typography
          variant="h6"
          component="div"
          style={{
            fontWeight: "bold",
            marginBottom: 6,
          }}
        >
          ${data.repairCost.toFixed(3)}
        </Typography>
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 0.5,
            }}
          >
            ⚙️ {data.damageType}
          </Typography>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 0.5,
            }}
          >
            🌍 ({latitude}, {longitude})
          </Typography>
        </Box>
        <Button
          variant="contained"
          color="primary"
          fullWidth
          style={{
            borderRadius: 6,
            marginTop: 12,
            padding: "8px 12px",
            textTransform: "none",
            fontWeight: "bold",
            fontSize: "0.875rem",
          }}
          onClick={() => onOpen(data)}
        >
          View Details
        </Button>
      </CardContent>
    </Card>
  );
};

export default CardView;
