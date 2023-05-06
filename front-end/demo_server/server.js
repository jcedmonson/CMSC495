const express = require("express");
var cors = require("cors");
const { response } = require("express");
const app = express();
const port = 5000;

app.use(cors());
app.use(express.json());

const users = [
  {
    userId: 0,
    username: "bdavis",
    first_name: "Cynthia",
    last_name: "Larson",
    email: "jose72@example.org",
    password: "M$1Kc)GA%O",
    token: "ACrazyToken0",
    connections: [],
  },
  {
    userId: 1,
    username: "xrios",
    first_name: "Richard",
    last_name: "Hunter",
    email: "chaneymathew@example.com",
    password: "+A1Owjtq1&",
    token: "ACrazyToken1",
    connections: [],
  },
  {
    userId: 2,
    username: "cynthiaallen",
    first_name: "Jack",
    last_name: "Miller",
    email: "uburns@example.com",
    password: "q7@BfwAh&%",
    token: "ACrazyToken2",
    connections: [],
  },
  {
    userId: 3,
    username: "michelle81",
    first_name: "James",
    last_name: "Sims",
    email: "garciajames@example.com",
    password: "#XW@1D2dej",
    token: "ACrazyToken3",
    connections: [],
  },
  {
    userId: 4,
    username: "lindsay04",
    first_name: "Maria",
    last_name: "Gomez",
    email: "xflowers@example.net",
    password: "_bB8FUlJ7U",
    token: "ACrazyToken4",
    connections: [],
  },
  {
    userId: 5,
    username: "gavinmarsh",
    first_name: "Brittany",
    last_name: "Trujillo",
    email: "pcontreras@example.com",
    password: "(5&JG8mCru",
    token: "ACrazyToken5",
    connections: [],
  },
  {
    userId: 6,
    username: "jedmonson",
    first_name: "Jacob",
    last_name: "Edmonson",
    email: "myemail@gmail.com",
    password: "myPassword",
    token: "ACrazyToken",
    connections: [],
  },
];

const posts = [
  {
    userId: 5,
    username: "gavinmarsh",
    postId: 0,
    content:
      "Foot strong discussion modern according government. Decide reason per friend some impact whether.Later lead stand. Cause learn fact easy computer person increase remain. Role your miss kind lay.",
    reactions: [],
    comments: []
  },
  {
    userId: 0,
    username: "bdavis",
    postId: 1,
    content:
      "Ask movement share real article. Inside three include employee.Thing hotel available people grow entire finish. Idea financial quickly despite once. Room protect down.",
    reactions: [],
    comments: []
  },
  {
    userId: 5,
    username: "gavinmarsh",
    postId: 2,
    content:
      "Expect prepare tonight current age while. Fast writer per sense. Book may site increase during.Similar industry sign sea study product. Ok civil newspaper air mission government day.",
    reactions: [],
    comments: []
  },
  {
    userId: 5,
    username: "gavinmarsh",
    postId: 3,
    content:
      "Do country design really between. Rate risk trial shoulder.Something office life move foreign difference. Official food American box will policy begin. Father fast sell road follow attorney.",
    reactions: [],
    comments: []
  },
  {
    userId: 5,
    username: "gavinmarsh",
    postId: 4,
    content:
      "Others family fire glass. Sea and they already.Act thousand central. Together a safe among seem. Police push show daughter.Night red pass thought want. Almost politics that hotel up show different.",
    reactions: [],
    comments: []
  },
  {
    userId: 0,
    username: "bdavis",
    postId: 5,
    content:
      "Relate order old nor will drive. Available there pressure write fish. Growth southern agree born box reach.Small like theory become foot. Question pull nor show food car always.",
    reactions: [],
    comments: []
  },
  {
    userId: 3,
    username: "michelle81",
    postId: 6,
    content:
      "Throughout break property environment.Win activity debate player. Trade feeling much let role. Situation run artist including character hour.Behind hour control. Water according run sure son.",
    reactions: [],
    comments: []
  },
  {
    userId: 0,
    username: "bdavis",
    postId: 7,
    content:
      "Sometimes little investment instead result across from. Drive go off true major less inside themselves. Stop against TV adult task statement cold dog.",
    reactions: [],
    comments: []
  },
  {
    userId: 2,
    username: "cynthiaallen",
    postId: 8,
    content:
      "Adult above they social visit simple. East consider knowledge town. Majority certain goal some politics edge look.We question another total serve. Expect training quickly many.",
    reactions: [],
    comments: []
  },
  {
    userId: 4,
    username: "lindsay04",
    postId: 9,
    content:
      "Involve left kind daughter avoid. Southern such rock customer. Know than control however reality class.Allow interview not attention. Standard trouble house hold whole daughter Democrat.",
    reactions: [],
    comments: []
  },
];

const simpleTokenAllocation = {
  token: "ACrazyToken",
};

// mimicks user login
app.post("/login", (req, res) => {
  const user = req.body;

  const getUser = (username, password) => {
    const incomingUser = users
      .map((u) => {
        return u.username;
      })
      .indexOf(username);
    if (incomingUser != -1 && users[incomingUser].password == password) {
      let userData = {};
      Object.keys(users[incomingUser])
        .filter((k) => k != "password")
        .forEach((k) => {
          userData[k] = users[incomingUser][k];
        });

      return userData;
    }
    return {};
  };

  const keys = Object.keys(user);
  if (keys.includes("username") && keys.includes("password")) {
    if (user.username != "" && user.password != "") {
      const userData = getUser(user.username, user.password);
      if (Object.keys(userData).length > 0) {
        res.status(200).json(userData);
      } else {
        res.sendStatus(403);
      }
    }
  } else {
    res.sendStatus(403);
  }
});

app.get("/users", (req, res) => {
  if (validToken(req)) {
    // need more here
    res.status(200).json(
      users.map((u) => {
        return {
          userId: u.userId,
          username: u.username,
          first_name: u.first_name,
          last_name: u.last_name,
        };
      })
    );
  } else {
    res.sendStatus(403);
  }
});

// mimicks user creation
app.post("/user", (req, res) => {
  const newUser = req.body;
  if (
    newUser.email != existingUser.email &&
    newUser.username != existingUser.email
  ) {
    users.push({
      userId: users.length,
      username: newUser.username,
      first_name: newUser.first_name,
      last_name: newUser.last_name,
      email: newUser.email,
      connections: [],
      password: newUser.password,
      token: "ANewToken",
    });
    res.sendStatus(201);
  } else {
    res.sendStatus(403);
  }
});

const validToken = (req) => {
  const token = req.headers.authorization;
  if (token.includes("Bearer ")) {
    const user = users.filter(
      (u) => u.token == req.headers.authorization.split(" ")[1]
    );

    return user.length == 1;
  }
  return false;
};

// get user data, used on refresh with token
app.get("/user", (req, res) => {
  const user = users.filter(
    (u) => u.token == req.headers.authorization.split(" ")[1]
  );
  user.length == 1 ? res.status(200).json(user[0]) : res.sendStatus(403);
});

app.post("/user/:uid/connection", (req, res) => {
  if (validToken(req)) {
    // need more here
    const user = users.filter((u) => {
      return u.userId == req.params.uid;
    });

    if (user.length == 1) {
      users[users.indexOf(user[0])].connections.push(req.body);
      res.sendStatus(201);
    } else {
      res.sendStatus(500);
    }
  } else {
    res.sendStatus(403);
  }
});

// mimicks token validation
app.get("/validToken", (req, res) => {
  if (validToken(req)) {
    // need more here
    res.sendStatus(200);
  } else {
    res.sendStatus(403);
  }
});

app.get("/posts", (req, res) => {
  if (validToken(req)) {
    const user = users.filter((u) => {
      return u.token == req.headers.authorization.split(" ")[1];
    });
    const connections = user[0].connections;
    const followedPosts = posts.filter((p) => {
      if (
        connections
          .map((k) => {
            return k.userId;
          })
          .includes(p.userId) || p.userId == user[0].userId
      ) {
        return p;
      }
    });

    // need more here
    res.status(200).json(
      followedPosts.sort((a, b) => {
        if (a.postId < b.postId) {
          return 1;
        }
        if (a.postId > b.postId) {
          return -1;
        }
      })
    );
  } else {
    res.sendStatus(403);
  }
});


app.get("/posts/:id", (req, res) => {
  if (validToken(req)) {
    const post = posts.filter((p) => { return p.postId == req.params.id})
    console.log(post)
    post.length == 1 ? res.status(200).json(post[0]) :
    res.sendStatus(404)
  } else {
    res.sendStatus(403);
  }
});

app.post("/posts", (req, res) => {
  if (validToken(req)) {
    const post = req.body;
    const newPost = {
      userId: post.userId,
      username: post.username,
      postId: posts.length,
      content: post.content,
      reactions: [],
    };
    posts.push(newPost);
    res.status(201).json(newPost);
  } else {
    res.sendStatus(403);
  }
});

app.post("/posts/:id/reaction", (req, res) => {
  const reaction = req.body;

  const id = req.params.id;

  // get user from token
  const user = users.filter(
    (u) => u.token == req.headers.authorization.split(" ")[1]
  );

  // get post
  const post = posts.filter((p) => p.postId == id);

  // add reaction
  if (user.length == 1 && post.length == 1) {
    post[0].reactions.push(reaction);
    res.sendStatus(201);
  } else {
    res.sendStatus(403);
  }
});


app.post("/posts/:id/comment", (req, res) => {
  const comment = req.body;
  const id = req.params.id;

  // get user from token
  const user = users.filter(
    (u) => u.token == req.headers.authorization.split(" ")[1]
  );

  // get post
  const post = posts.filter((p) => p.postId == id);

  // add reaction
  if (user.length == 1 && post.length == 1) {
    post[0].reactions.push(comment);
    res.sendStatus(201);
  } else {
    res.sendStatus(403);
  }
});

app.listen(port, () => {
  console.log("ready");
});
