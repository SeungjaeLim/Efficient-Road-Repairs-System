import React from "react";
import {
  Modal,
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";

const ModalView = ({ open, handleClose, data }) => {
  if (!data) return null;

  const geoLocation = data.geoLocation || "urn:epc:id:geo:37.7750,-122.4195";
  const coordinates = geoLocation.split(":").pop().split(",");
  const latitude = parseFloat(coordinates[0]).toFixed(3); // 소수점 6자리로 고정
  const longitude = parseFloat(coordinates[1]).toFixed(3);

  return (
    <Modal open={open} onClose={handleClose}>
      <Box
        sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: "80%",
          maxWidth: 800,
          bgcolor: "background.paper",
          boxShadow: 24,
          borderRadius: 4,
          p: 3,
        }}
      >
        {/* Receipt 제목 */}
        <Typography
          variant="h5"
          component="div"
          sx={{
            textAlign: "center",
            marginBottom: 2,
            fontWeight: "bold",
          }}
        >
          🧾 Receipt 🧾
        </Typography>

        {/* 상단 정보: 한 줄에 정렬 */}
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: 2,
          }}
        >
            <Typography
            variant="body1"
            component="div"
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 1,
              fontWeight: "normal",
            }}
          >
            ⚙️ {data.damageType}
          </Typography>
          <Typography
            variant="body1"
            component="div"
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 1,
              fontWeight: "normal",
            }}
          >
            🌍 ({latitude}, {longitude})
          </Typography>
          
          <Typography
            variant="body1"
            component="div"
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 1,
              fontWeight: "normal",
            }}
          >
            📐 W: {data.dimensions.Width.toFixed(2)}, H: {data.dimensions.Height.toFixed(2)}
          </Typography>
        </Box>

        {/* 표 아래로 이동 */}
        <TableContainer
          component={Paper}
          sx={{
            borderRadius: 2,
            boxShadow: "0 2px 8px rgba(0, 0, 0, 0.1)",
          }}
        >
          <Table>
            <TableHead>
              <TableRow sx={{ backgroundColor: "#f5f5f5" }}>
                <TableCell>Description</TableCell>
                <TableCell align="right">Quantity</TableCell>
                <TableCell align="right">Unit Price</TableCell>
                <TableCell align="right">Total Price</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.repairItems.map((item, index) => (
                <TableRow key={index}>
                  <TableCell>{item.ItemDescription || "Unknown"}</TableCell>
                  <TableCell align="right">
                    {item.Quantity ? item.Quantity.toFixed(2) : "N/A"}
                  </TableCell>
                  <TableCell align="right">
                    ${item.UnitPrice ? item.UnitPrice.toFixed(2) : "N/A"}
                  </TableCell>
                  <TableCell align="right">
                    ${item.TotalPrice ? item.TotalPrice.toFixed(2) : "N/A"}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Modal>
  );
};

export default ModalView;
