
class Cube {
  static MOVES = [
    "U2", "U'", "U",
    "D2", "D'", "D",
    "R2", "R'", "R",
    "L2", "L'", "L",
    "F2", "F'", "F",
    "B2", "B'", "B"
  ];

  static COLORS = { 'w': 0, 'r': 1, 'g': 2, 'o': 3, 'b': 4, 'y': 5 };
  static R_COLORS = { '0': 'w', '1': 'r', '2': 'g', '3': 'o', '4': 'b', '5': 'y' };
  static SIDES = {
    'top': 0,
    'left': 1,
    'back': 2,
    'right': 3,
    'front': 4,
    'bottom': 5
  };

  static RELATIONS = {
    'top': { 'right': 4, 'front': 6, 'left': 0, 'back': 2 },
    'left': { 'front': 4, 'bottom': 4, 'back': 4, 'top': 4 },
    'back': { 'right': 6, 'top': 6, 'left': 6, 'bottom': 2 },
    'right': { 'back': 0, 'bottom': 0, 'front': 0, 'top': 0 },
    'front': { 'top': 2, 'right': 2, 'bottom': 6, 'left': 2 },
    'bottom': { 'right': 0, 'back': 6, 'left': 4, 'front': 2 }
  };

  constructor(code = "") {
    this.state = Array(6 * 9).fill().map((_, i) => Math.floor(i / 9));
    if (code !== "") {
      for (let i = 0; i < code.length; i++) {
        this.state[i] = parseInt(code.charAt(i));
      }
    }
  }

  copy() {
    return new Cube(this.code());
  }

  code() {
    let txt = "";
    for (let i = 0; i < this.state.length; i++) {
      txt += this.state[i];
    }
    return txt;
  }

  scramble(text = "") {
    if (text === "") {
      let moves = [];
      for (let i = 0; i < 10; i++) {
        const m = Cube.MOVES[Math.floor(Math.random() * Cube.MOVES.length)];
        moves.push(m);
        this.move(m);
      }
      return moves.join(" ");
    }
    for (const move of text.split(" ")) {
      this.move(move);
    }
  }

  // move method
move(moveName) {
    // if multiple moves
    if (moveName.length > 2) {
        for (const move of moveName.split(" ")) {
            this.move(move);
        }
        return;
    }

    if (!Cube.MOVES.includes(moveName)) {
        return 1;
    }

    let side = null;
    if (moveName[0] === "U") {
        side = 'top';
    }
    if (moveName[0] === "L") {
        side = 'left';
    }
    if (moveName[0] === "B") {
        side = 'back';
    }
    if (moveName[0] === "R") {
        side = 'right';
    }
    if (moveName[0] === "F") {
        side = 'front';
    }
    if (moveName[0] === "D") {
        side = 'bottom';
    }

    let turns = 1;
    if (moveName.length === 2) {
        if (moveName[1] === '2') {
            turns = 2;
        } else if (moveName[1] === "'") {
            turns = 3;
        }
    }

    // turn face
    for (let i = 0; i < turns; i++) {
        const cary1 = this.state[Cube.SIDES[side] * 9 + 6];
        const cary2 = this.state[Cube.SIDES[side] * 9 + 7];

        for (let j = 0; j < 3; j++) {
            this.state[Cube.SIDES[side] * 9 + (2 - j) * 2 + 2] = this.state[Cube.SIDES[side] * 9 + (2 - j) * 2];
            this.state[Cube.SIDES[side] * 9 + (2 - j) * 2 + 3] = this.state[Cube.SIDES[side] * 9 + (2 - j) * 2 + 1];
        }

        this.state[Cube.SIDES[side] * 9 + 0] = cary1;
        this.state[Cube.SIDES[side] * 9 + 1] = cary2;
    }

    // turn sides
    for (let i = 0; i < turns; i++) {
        const sides = Object.entries(Cube.RELATIONS[side]);
        const cary1 = this.state[Cube.SIDES[sides[1][0]] * 9 + (sides[1][1] + 0) % 8];
        const cary2 = this.state[Cube.SIDES[sides[1][0]] * 9 + (sides[1][1] + 1) % 8];
        const cary3 = this.state[Cube.SIDES[sides[1][0]] * 9 + (sides[1][1] + 2) % 8];
        for (let j = 0; j < sides.length - 1; j++) {
            const s = sides[(4 - j) % 4];
            const next_s = sides[(4 - j + 1) % 4];
            
            this.state[Cube.SIDES[next_s[0]] * 9 + (next_s[1] + 0) % 8] = this.state[Cube.SIDES[s[0]] * 9 + (s[1] + 0) % 8];
            this.state[Cube.SIDES[next_s[0]] * 9 + (next_s[1] + 1) % 8] = this.state[Cube.SIDES[s[0]] * 9 + (s[1] + 1) % 8];
            this.state[Cube.SIDES[next_s[0]] * 9 + (next_s[1] + 2) % 8] = this.state[Cube.SIDES[s[0]] * 9 + (s[1] + 2) % 8];
          }            
          const next_s = sides[(4 - 3 + 1) % 4];
          this.state[Cube.SIDES[next_s[0]] * 9 + (next_s[1] + 0) % 8] = cary1;
          this.state[Cube.SIDES[next_s[0]] * 9 + (next_s[1] + 1) % 8] = cary2;
          this.state[Cube.SIDES[next_s[0]] * 9 + (next_s[1] + 2) % 8] = cary3;
        }
      }
    }

module.exports = Cube;
