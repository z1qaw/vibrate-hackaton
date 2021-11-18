// @ts-nocheck
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var roomDetails = {}
var roomSocket = null
var selfUser = {}
var roomSlug = ''


function fallbackCopyTextToClipboard(text) {
  var textArea = document.createElement("textarea");
  textArea.value = text;

  // Avoid scrolling to bottom
  textArea.style.top = "0";
  textArea.style.left = "0";
  textArea.style.position = "fixed";

  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    var successful = document.execCommand('copy');
    var msg = successful ? 'successful' : 'unsuccessful';
    console.log('Fallback: Copying text command was ' + msg);
  } catch (err) {
    console.error('Fallback: Oops, unable to copy', err);
  }

  document.body.removeChild(textArea);
}
function copyTextToClipboard(text) {
  if (!navigator.clipboard) {
    fallbackCopyTextToClipboard(text);
    return;
  }
  navigator.clipboard.writeText(text).then(function () {
    console.log('Async: Copying to clipboard was successful!');
  }, function (err) {
    console.error('Async: Could not copy text: ', err);
  });
}


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

  var copyLinkButton = document.querySelector('#copy-link-button')
  var copyLinkPopover = new bootstrap.Popover(
    copyLinkButton,
    {
      animation: true,
      content: 'Link copied!',
      delay: { hide: 100, show: 100 },
    }
  )

  copyLinkButton.addEventListener('click', async () => {
    copyTextToClipboard(window.location.href)
    setTimeout(() => {
      copyLinkPopover.hide()
    }, 3000)
  })


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
      case 'vibrate':
        vibrationQueue.push(data.user_id)
    }
  }
}

var vibrationQueue = []



function showUserVibration(userId) {
  const userElement = document.querySelector(`li.user-card[userId="${userId}"]`)
  // Анимируем элемент юзера
  userElement.animate(
    [
      { backgroundColor: 'rgb(255, 255, 255)' },
      { backgroundColor: 'rgb(37, 127, 211, 0.3)' },
      { backgroundColor: 'rgb(255, 255, 255)' },

    ],
    {
      duration: 180,
      iterations: 2
    }
  )
  // Вибрируем
  window.navigator.vibrate([180, 30, 180])
}

setInterval(async () => {
  if (vibrationQueue.length > 0) {
    showUserVibration(vibrationQueue.shift())
  }
}, 500)

async function updateUsersList() {
  var response = await fetch(`/api/get_room_members/${roomSlug}`)
  var data = await response.json()
  var usersElWrappers = document.querySelector('#users-list')
  usersElWrappers.innerText = ''
  data.map((user) => {
    singleUserElWrapper = document.createElement('li')
    singleUserElWrapper.classList.add('user-element')
    singleUserElWrapper.setAttribute('userId', user.id)
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
    for (className of 'user-card list-group-item d-flex align-items-center'.split(' ')) {
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