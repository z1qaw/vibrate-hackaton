// @ts-nocheck
async function postData(url = '', data = {}, csrf_token = null) {
  var response = await fetch(url, {
    method: 'POST',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token,
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body: JSON.stringify(data)
  })
}

function arraysEqual(a1, a2) {
  return JSON.stringify(a1) == JSON.stringify(a2);
}

var rooms = []
var choosedRoom = null
var roomsContainer = document.querySelector('#rooms-container')

var roomEnterModalEl = document.getElementById('roomEnterModal')
var roomEnterModal = new bootstrap.Modal(roomEnterModalEl, {
  keyboard: false
})

roomEnterModalEl.addEventListener('show.bs.modal', function (event) {
  var modalTitle = roomEnterModalEl.querySelector('.modal-title')
  var modalEnterButton = roomEnterModalEl.querySelector('#enter_room_button')
  var usernameInput = roomEnterModalEl.querySelector('#username')
  var csrfToken = roomEnterModalEl.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value')
  modalEnterButton.addEventListener('click', async (e) => {
    await postData('/api/set_roommember_nickname/', {
      username: usernameInput.value
    }, csrfToken)
    window.location.replace(`room/${choosedRoom.slug}`)
  })
  usernameInput.addEventListener('keyup', (e) => {
    if (e.keyCode === 13) {
      modalEnterButton.click()
    }
  })

  modalTitle.textContent = 'Войти в комнату ' + choosedRoom.name
})

async function apiGetRooms() {
  var response = await fetch('/api/get_rooms')
  return await response.json()
}

function setRooms() {
  var containerChildren = []
  for (room of rooms) {
    var roomEl = document.createElement('li')
    for (className of 'list-group-item d-flex justify-content-between align-items-center'.split(' ')) {
      roomEl.classList.add(className)
    }
    roomEl.innerText += room.name
    roomEl.setAttribute('roomslug', room.slug)

    var usersCounter = document.createElement('span')
    for (className of 'badge bg-primary rounded-pill'.split(' ')) {
      usersCounter.classList.add(className)
    }
    usersCounter.innerText += room.current_members.length + ' участников'
    roomEl.appendChild(usersCounter)

    roomEl.addEventListener('click', (e) => {
      console.log('target', rooms.filter(r => r.slug == e.target.getAttribute('roomslug')))
      choosedRoom = rooms.filter(r => { return r.slug == e.target.getAttribute('roomslug') })[0]
      console.log('choosedRoom', choosedRoom)
      roomEnterModal.show()
    })

    containerChildren.push(roomEl)
  }
  roomsContainer.textContent = ''
  for (roomEl of containerChildren) {
    roomsContainer.appendChild(roomEl)
    console.log('appendChild')
  }
}

var init = async () => {
  rooms = await apiGetRooms()
  setRooms()
}

init()

setInterval(async () => {
  var freshRooms = await apiGetRooms()
  if (!arraysEqual(freshRooms, rooms)) {
    console.log('not equel', rooms, freshRooms)
    rooms = freshRooms
    setRooms()
  }
}, 3000)
