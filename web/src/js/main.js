var loadedRegistry = [];
var leftVideoRef;
var middleVideoRef;
var rightVideoRef;

var body = document.body;
var isFullScreen = false;

var randomItem = function (array) {
  var index = Math.floor(Math.random() * array.length);
  var item = array[index];
  var filter = loadedRegistry.filter((r) => r.id === item.id);
  var isRandomFound = filter.length === 0;

  while (!isRandomFound) {
    index = Math.floor(Math.random() * array.length);
    item = array[index];
    filter = loadedRegistry.filter((r) => r.id === item.id);
    isRandomFound = filter.length === 0;
  }

  return item;
};

var registry = [
  {
    id: "Pond",
    videos: [
      {
        id: 1,
        path: "/data/Pond/PondDay1.mp4",
      },
    ],
  },
  {
    id: "River",
    videos: [
      {
        id: 1,
        path: "/data/River/RiverDay1.mp4",
      },
    ],
  },
  {
    id: "Silo",
    videos: [
      {
        id: 1,
        path: "/data/Silo/SiloDay1.mp4",
      },
      {
        id: 2,
        path: "/data/Silo/SiloDay2.mp4",
      },
      {
        id: 3,
        path: "/data/Silo/SiloDay3.mp4",
      },
    ],
  },
  {
    id: "Treehouse",
    videos: [
      {
        id: 1,
        path: "/data/Treehouse/TreeHouseDay1.mp4",
      },
      {
        id: 2,
        path: "/data/Treehouse/TreeHouseDay2.mp4",
      },
      {
        id: 3,
        path: "/data/Treehouse/TreeHouseDay3.mp4",
      },
    ],
  },
  {
    id: "Van",
    videos: [
      {
        id: 1,
        path: "/data/Van/VanDay1.mp4",
      },
      {
        id: 2,
        path: "/data/Van/VanDay2.mp4",
      },
      {
        id: 3,
        path: "/data/Van/VanDay3.mp4",
      },
    ],
  },
];

var loadInitialVideos = function (callback) {
  while (true) {
    var random = randomItem(registry);
    console.log("Found random scene to load --> " + random.id, random);
    loadedRegistry.push(random);
    console.log("New registry count " + loadedRegistry.length, loadedRegistry);

    if (loadedRegistry.length === 3) {
      callback();
      break;
    }
  }
};

window.onload = function () {
  console.log("Loaded registry count " + loadedRegistry.length, loadedRegistry);

  leftVideoRef = document.getElementById("left-player");
  middleVideoRef = document.getElementById("middle-player");
  rightVideoRef = document.getElementById("right-player");

  loadInitialVideos(function () {
    if (loadedRegistry.length === 3) {
      console.info("Let's begin");

      if (!leftVideoRef || !middleVideoRef || !rightVideoRef) {
        console.info("Missing one of the players. Stopping...");
        return;
      }

      console.info("Found all 3 players. Initiaing...");

      for (var i = 0; i < loadedRegistry.length; ++i) {
        var video = loadedRegistry[i];
        var source = document.createElement("source");
        source.src = video.videos[0].path;

        if (i === 0) {
          leftVideoRef.appendChild(source);
          leftVideoRef.load();
          leftVideoRef.onended = () => {
            alert();
          };
        }

        if (i === 1) {
          middleVideoRef.appendChild(source);
          middleVideoRef.load();
        }

        if (i === 2) {
          rightVideoRef.appendChild(source);
          rightVideoRef.load();
        }
      }
    }
  });
};

document.onkeypress = function (e) {
  e = e || window.event;
  // use e.keyCode
  console.warn(e.keyCode);
  if (e.keyCode === 121) {
    if (!isFullScreen) {
      body.requestFullscreen();
      isFullScreen = true;
    } else {
      document.exitFullscreen();
      isFullScreen = false;
    }
  }
};
