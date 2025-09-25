const BASE_URL = "http://10.200.67.161:5000"; // backend LAN IP + port

export const getTestData = async () => {
  const response = await fetch(`${BASE_URL}/api/test`);
  if (!response.ok) throw new Error("Network response was not ok");
  return response.json();
};
