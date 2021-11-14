// @ts-nocheck
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var roomDetails = {}
var roomSocket = null
var selfUser = {}
var roomSlug = ''


async function init() {
  var locationPathnameArr = window.location.pathname.split('/')
  roomSlug = locationPathnameArr[locationPathnameArr.length - 1]
  var response = await fetch(`/api/get_room_details/${roomSlug}/`)
  roomDetails = await response.json()

  var response = await fetch('/api/get_me/')
  selfUser = await response.json()
  document.querySelector('#title').innerText = roomDetails.name
  roomSocket = new WebSocket(
    `${ws_scheme}://${window.location.host}/ws/room/${roomDetails.slug}/`
  )

  roomSocket.onclose = (e) => {
    console.log('on_close', e)
  }
  roomSocket.onmessage = (e) => {
    const data = JSON.parse(e.data)
    console.log('on_message', data)
    switch (data.action) {
      case 'user_connect':
        updateUsersList()
        break
      case 'user_disconnect':
        updateUsersList()
        break
    }
  }
}

async function updateUsersList() {
  var response = await fetch(`/api/get_room_members/${roomSlug}`)
  var data = await response.json()
  var usersElWrappers = document.querySelector('#users-list')
  usersElWrappers.innerText = ''
  data.map((user) => {
    singleUserElWrapper = document.createElement('li')
    singleUserElWrapper.classList.add('user-element')
    singleUserElWrapper.innerText = user.room_nickname || 'Аноним'
    if (user.id === selfUser.id) {
      selfUserSpan = document.createElement('span')
      selfUserSpan.innerText = 'Вы'
      for (className of 'badge bg-secondary'.split(' ')) {
        selfUserSpan.classList.add(className)
      }
      selfUserSpan.id = 'self-user-span'
      singleUserElWrapper.appendChild(selfUserSpan)
    }
    for (className of 'list-group-item d-flex align-items-center'.split(' ')) {
      singleUserElWrapper.classList.add(className)
    }
    usersElWrappers.appendChild(singleUserElWrapper)
  })
}

init()
updateUsersList()

var sendVibrationButton = document.querySelector('#send_vibration')
sendVibrationButton.addEventListener('click', () => {
  console.log('send', {
    user_id: selfUser.id,
    action: 'vibrate',
  })
  roomSocket.send(JSON.stringify(
    {
      type: 'message',
      user_id: selfUser.id,
      action: 'vibrate',
      room_slug: roomDetails.slug,
    }
  ))
})