const base = {
  baseUrl: "http://127.0.0.1:8000",
  chengpin: "/api/blueberrypai/getChengpinDetails.php",
  localTEST: "/api/getData",
  login: "/api/login",
  checkIn: "/api/rooms/checkIn",
  checkOut: "/api/rooms/checkOut",
  turnOn: "/api/turn_on",
  turnOff: "/api/turn_off",
  setTemperature: "/api/setTemperature",
  setTemperatureInit: "/api/setTemperature_init",
  setSpeed: "/api/setSpeed",
  queryRoomInfo: "/api/query_room_info",
  updateRooms: "/api/rooms/updateRooms",
  roomList: "/api/form/roomList",
  getForm: "/api/form/rep",
  send_cur_temp: "/api/send_current_temp",
  detail: "/api/detail_bill",
  bill: "/api/query_room_bill",
  setMode: "/api/setMode",
}

export default base;