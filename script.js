window.onload = function () {
  var poolTable = document.getElementById('pool-table-svg');
  var canvas = document.getElementById('canvas');
  var ctx = canvas.getContext('2d');

  // Resize canvas to cover the whole window
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  window.current_player = 1
  shot_result = {
    game_over: false,
    winner: 0,
    next_player: 1,
    player_one_ball_set: [],
    player_two_ball_set: [],
    player_one_ball_set_name: "",
    player_two_ball_set_name: ""
  };
  window.last_shot_result = shot_result;
  // Get the entered values from the URL parameters
  var gameName = get_url_parameter('game-name');
  var playerOne = get_url_parameter('player-one');
  var playerTwo = get_url_parameter('player-two');

  startNewGame({ game_name: gameName, player_one: playerOne, player_two: playerTwo });

  // Flag to track if cue ball is clicked
  let cueBallClicked = false;
  // Pool table rectangle
  var tableRect = poolTable.getBoundingClientRect();

  // Redraw canvas when window is resized
  window.addEventListener('resize', function () {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    // Call any drawing function here to redraw canvas content if needed
    tableRect = poolTable.getBoundingClientRect();
    window.cueBallPosition = getCueBallPosition(window.cueBall);
  });

  // Listen for mouse movements
  canvas.addEventListener('mousemove', (e) => {
    if (cueBallClicked) {
      drawLine(e.clientX, e.clientY);
    } else {
      if (e.clientX >= window.cueBallPosition.x - window.cueBallPosition.radius &&
        e.clientX <= window.cueBallPosition.x + window.cueBallPosition.radius &&
        e.clientY >= window.cueBallPosition.y - window.cueBallPosition.radius &&
        e.clientY <= window.cueBallPosition.y + window.cueBallPosition.radius) {
        drawCueBallMouseOver();
      } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
    }
  });

  // Listen for mouse click on the cue ball
  canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    // Check if click is on the cue ball
    // Adjust these values based on cue ball size
    if (clickX >= window.cueBallPosition.x - window.cueBallPosition.radius &&
      clickX <= window.cueBallPosition.x + window.cueBallPosition.radius &&
      clickY >= window.cueBallPosition.y - window.cueBallPosition.radius &&
      clickY <= window.cueBallPosition.y + window.cueBallPosition.radius) {
      cueBallClicked = true;
    }
  });

  // Event listener to handle mouse up event
  canvas.addEventListener('mouseup', function (event) {
    if (cueBallClicked) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      var dx = event.clientX - window.cueBallPosition.x;
      var dy = event.clientY - window.cueBallPosition.y;
      console.log('Length of the drawing line:', { dx, dy });

      // Calculate percentage of line length relative to maxLength
      var maxLength = tableRect.width * 0.75;
      var percentageX = (Math.min(maxLength, Math.abs(dx)) / maxLength) * 100;
      var percentageY = (Math.min(maxLength, Math.abs(dy)) / maxLength) * 100;
      console.log('Percentage of line length:', { x: percentageX + '%', y: percentageY + '%' });

      // Calculate initial X,Y velocity based on percentage
      var velocityX = ((percentageX / 100) * 10000) * (dx < 0 ? 1 : -1);
      var velocityY = ((percentageY / 100) * 10000) * (dy < 0 ? 1 : -1);
      console.log('Initial velocity:', { velocityX: velocityX + ' mm/s', velocityY: velocityY + 'mm/s' });
      cueBallClicked = false;

      var shotData = {
        "xvel": velocityX,
        "yvel": velocityY
      };
      doShoot(shotData);
    }
  });

  // Function to draw a line from the starting point to the current mouse position
  function drawLine(mouseX, mouseY) {
    // Calculate distance from starting point to current mouse position
    var dx = mouseX - window.cueBallPosition.x;
    var dy = mouseY - window.cueBallPosition.y;
    var distance = Math.sqrt(dx * dx + dy * dy);
    // Limit the size of the line to a maximum value
    var maxLength = tableRect.width * 0.75;
    if (distance > maxLength) {
      // Calculate scaled down distance to fit within maxLength
      var scale = maxLength / distance;
      dx *= scale;
      dy *= scale;
    }
    // Draw the line
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.moveTo(window.cueBallPosition.x, window.cueBallPosition.y);
    ctx.lineTo(window.cueBallPosition.x + dx, window.cueBallPosition.y + dy);
    ctx.strokeStyle = 'red'; // color of the line
    ctx.lineWidth = 2; // thickness of the line
    ctx.stroke();
  }

  function drawCueBallMouseOver() {
    // Draw cue ball
    ctx.beginPath();
    ctx.arc(window.cueBallPosition.x, window.cueBallPosition.y, window.cueBallPosition.radius * 1.5, 0, Math.PI * 2);
    ctx.fillStyle = 'white';
    ctx.fill();
  }

  function getCueBallPosition(cueBall) {
    // Get the bounding box of the circle
    if (cueBall == undefined || cueBall == null) {
      return { x: 0, y: 0, radius: 0, present: false };
    }
    var circleBox = cueBall.getBoundingClientRect();
    var centerX = circleBox.left + circleBox.width / 2;
    var centerY = circleBox.top + circleBox.height / 2;
    return { x: centerX, y: centerY, radius: circleBox.width / 2, present: true };
  }

  function startNewGame(data) {
    $.ajax({
      url: '/start-new-game',
      method: 'POST',
      data: JSON.stringify(data),
      async: false,
      contentType: 'application/json',
      success: function (data) {
        window.current_player = data.current_player;
        window.game_name = data.game_name;
        window.player_one = data.player_one;
        window.player_two = data.player_two;
        document.getElementById('player-one-name').innerText = data.player_one;
        document.getElementById('player-two-name').innerText = data.player_two;
        poolTable.innerHTML = data.rack;
        set_cue_ball('#pool-table-svg > g > .cue-ball');
        if (window.current_player == 1) {
          document.querySelector('.player-one-container > .current-player').style.visibility = 'visible';
          document.querySelector('.player-two-container > .current-player').style.visibility = 'hidden';
        } else {
          document.querySelector('.player-one-container > .current-player').style.visibility = 'hidden';
          document.querySelector('.player-two-container > .current-player').style.visibility = 'visible';
        }
        new_game = {
          current_player: window.current_player,
          game_name: window.game_name,
          player_one: window.player_one,
          player_two: window.player_two
        };
        console.log('New Game Started:', new_game);
      },
      error: function (xhr, status, error) {
        console.error('Error fetching data:', error);
      }
    });
  }

  function doShoot(data) {
    console.log('Shoot request sent to the server to calculate animation...');

    document.getElementById('overlay').style.display = 'block';
    document.getElementById('canvas').style.display = 'none';

    $.ajax({
      url: '/shoot',
      method: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json',
      success: function (data) {
        console.log('...Animation is ready. Total frames = ' + data.animation_frames.length);
        shot_result = {
          game_over: data.game_over,
          winner: data.winner,
          next_player: data.next_player,
          player_one_ball_set: data.player_one_ball_set,
          player_two_ball_set: data.player_two_ball_set,
          player_one_ball_set_name: data.player_one_ball_set_name,
          player_two_ball_set_name: data.player_two_ball_set_name,
          winner_name: data.winner_name
        };
        window.current_player = data.next_player;
        if (window.current_player == 1) {
          document.querySelector('.player-one-container > .current-player').style.visibility = 'visible';
          document.querySelector('.player-two-container > .current-player').style.visibility = 'hidden';
        } else {
          document.querySelector('.player-one-container > .current-player').style.visibility = 'hidden';
          document.querySelector('.player-two-container > .current-player').style.visibility = 'visible';
        }
        console.log('Shot Result:', shot_result);
        window.last_shot_result = shot_result;
        if (data.animation_frames.length > 0) {
          animate_frames("#pool-table-svg", data.animation_frames);
        } else {
          console.error('Something went wrong. Server returned 0 frames for the last shot.');
        }
      },
      error: function (xhr, status, error) {
        console.error('Error fetching data:', error);
      },
      complete: function (xhr, status) {
        document.getElementById('overlay').style.display = 'none';
        document.getElementById('canvas').style.display = 'block';
      }
    });
  }
};

// Function to get URL parameter by name
function get_url_parameter(name) {
  name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
  var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
  var results = regex.exec(location.search);
  return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

function set_cue_ball(element) {
  window.cueBall = document.querySelector(element);
  window.cueBallPosition = { x: 0, y: 0, radius: 0, present: false };
  if (window.cueBall !== undefined && window.cueBall !== null) {
    var circleBox = window.cueBall.getBoundingClientRect();
    var centerX = circleBox.left + circleBox.width / 2;
    var centerY = circleBox.top + circleBox.height / 2;
    window.cueBallPosition = { x: centerX, y: centerY, radius: circleBox.width / 2, present: true };
  }
}

function animate_frames(element, data) {
  console.log('Animation started...');
  document.getElementById('overlay').style.display = 'none';
  document.querySelector(element).innerHTML = data.join('');

  var currentIndex = 0;
  var g_elements = document.querySelectorAll(element + ' > g');
  g_elements[currentIndex].style.display = 'block';
  set_cue_ball(element + ' > g:last-child > .cue-ball');

  function animate_svg_frames() {
    g_elements[currentIndex].style.display = 'none';
    currentIndex = (currentIndex + 1) % g_elements.length;
    g_elements[currentIndex].style.display = 'block';

    if (currentIndex === g_elements.length - 1) {
      clearInterval(window.animate_svg_interval_id);
      console.log('...Animation finished');
      var player_one_set = document.getElementById('player-one-set');
      player_one_set.style.backgroundColor = 'transparent';
      if (window.last_shot_result.player_one_ball_set_name === 'High') {
        player_one_set.style.backgroundColor = 'red';
      }
      else if (window.last_shot_result.player_one_ball_set_name === 'Low') {
        player_one_set.style.backgroundColor = 'blue';
      }
      player_one_set.innerText = window.last_shot_result.player_one_ball_set_name;
      var player_two_set = document.getElementById('player-two-set');
      player_two_set.style.backgroundColor = 'transparent';
      if (window.last_shot_result.player_two_ball_set_name === 'High') {
        player_two_set.style.backgroundColor = 'red';
      }
      else if (window.last_shot_result.player_two_ball_set_name === 'Low') {
        player_two_set.style.backgroundColor = 'blue';
      }
      player_two_set.innerText = window.last_shot_result.player_two_ball_set_name;

      if (window.last_shot_result.game_over === true) {

      }
      if (window.last_shot_result.game_over === true && window.last_shot_result.winner > 0) {
        document.querySelector('.game-over-container').innerHTML = '<h3>GAME OVER&nbsp;&nbsp;&nbsp; Winner is ' + window.last_shot_result.winner_name + '</h3>';
        document.querySelector('.game-over-container').style.visibility = 'visible';
      } else {
        document.querySelector('.game-over-container').style.visibility = 'hidden';
        document.querySelector('.game-over-container').innerHTML = '';
      }

      return false;
    }
  }

  window.animate_svg_interval_id = setInterval(animate_svg_frames, 10);
  return false;
};