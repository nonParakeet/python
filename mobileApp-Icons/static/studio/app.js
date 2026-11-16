(() => {
  const palettes = {
    "#e78050": ["#f5ae78", "#df754e", "#8d402d", "#552a25"],
    "#8f79df": ["#c2b1ff", "#9179e4", "#5944a2", "#342c66"],
    "#4f9bd1": ["#a6dcf6", "#519dd5", "#28618f", "#1c3e60"],
    "#58a88a": ["#a2e3bf", "#57aa88", "#2d7057", "#20493e"],
    "#d6aa59": ["#f4d18a", "#d9aa56", "#946b31", "#5a462e"],
  };
  const state = { icon: "phone", color: "#e78050" };
  const mainCanvas = document.querySelector("#main-preview");
  const iconGrid = document.querySelector("#icon-grid");
  const swatches = document.querySelector("#swatches");
  const selectedName = document.querySelector("#selected-name");
  const downloadButton = document.querySelector("#download-button");
  const downloadNote = document.querySelector("#download-note");
  const names = {
    phone: "Phone",
    messages: "Messages",
    contacts: "Contacts",
    camera: "Camera",
    maps: "Maps",
    music: "Music",
    shield: "Shield",
    folder: "Folder",
  };

  function roundedRect(ctx, x, y, width, height, radius) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
  }

  function drawGlyph(ctx, icon) {
    ctx.save();
    ctx.strokeStyle = "#fff8eb";
    ctx.fillStyle = "#fff8eb";
    ctx.lineWidth = 19;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";

    if (icon === "phone") {
      ctx.beginPath();
      ctx.moveTo(187, 157);
      ctx.quadraticCurveTo(172, 171, 183, 197);
      ctx.quadraticCurveTo(211, 267, 290, 302);
      ctx.quadraticCurveTo(310, 311, 325, 293);
      ctx.lineTo(342, 272);
      ctx.quadraticCurveTo(346, 266, 337, 259);
      ctx.lineTo(301, 236);
      ctx.quadraticCurveTo(294, 232, 287, 240);
      ctx.lineTo(271, 258);
      ctx.quadraticCurveTo(235, 239, 218, 204);
      ctx.lineTo(236, 187);
      ctx.quadraticCurveTo(242, 180, 236, 172);
      ctx.lineTo(213, 139);
      ctx.quadraticCurveTo(208, 132, 201, 140);
      ctx.closePath();
      ctx.fill();
    } else if (icon === "messages") {
      roundedRect(ctx, 155, 151, 210, 154, 43);
      ctx.fill();
      ctx.beginPath();
      ctx.moveTo(191, 292);
      ctx.lineTo(174, 338);
      ctx.lineTo(236, 304);
      ctx.closePath();
      ctx.fill();
      [215, 260, 305].forEach((x) => {
        ctx.beginPath();
        ctx.arc(x, 227, 8, 0, Math.PI * 2);
        ctx.fillStyle = "#ba7252";
        ctx.fill();
      });
    } else if (icon === "contacts") {
      ctx.beginPath();
      ctx.arc(256, 200, 39, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.moveTo(166, 335);
      ctx.bezierCurveTo(172, 278, 211, 256, 256, 256);
      ctx.bezierCurveTo(302, 256, 340, 278, 346, 335);
      ctx.quadraticCurveTo(346, 346, 334, 346);
      ctx.lineTo(178, 346);
      ctx.quadraticCurveTo(166, 346, 166, 335);
      ctx.fill();
    } else if (icon === "camera") {
      roundedRect(ctx, 144, 178, 224, 159, 35);
      ctx.fill();
      roundedRect(ctx, 192, 154, 70, 32, 13);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(256, 257, 48, 0, Math.PI * 2);
      ctx.fillStyle = "#ad7050";
      ctx.fill();
      ctx.beginPath();
      ctx.arc(256, 257, 27, 0, Math.PI * 2);
      ctx.fillStyle = "#fff8eb";
      ctx.fill();
      ctx.beginPath();
      ctx.arc(327, 202, 9, 0, Math.PI * 2);
      ctx.fillStyle = "#f3bd83";
      ctx.fill();
    } else if (icon === "maps") {
      ctx.beginPath();
      ctx.moveTo(256, 349);
      ctx.bezierCurveTo(234, 317, 174, 251, 174, 209);
      ctx.arc(256, 209, 82, Math.PI, 0, false);
      ctx.bezierCurveTo(338, 251, 278, 317, 256, 349);
      ctx.closePath();
      ctx.fill();
      ctx.beginPath();
      ctx.arc(256, 208, 31, 0, Math.PI * 2);
      ctx.fillStyle = "#a96c4b";
      ctx.fill();
      ctx.beginPath();
      ctx.arc(256, 208, 17, 0, Math.PI * 2);
      ctx.fillStyle = "#fff8eb";
      ctx.fill();
    } else if (icon === "music") {
      ctx.beginPath();
      ctx.moveTo(236, 177);
      ctx.lineTo(236, 289);
      ctx.bezierCurveTo(215, 275, 175, 285, 172, 315);
      ctx.bezierCurveTo(169, 342, 216, 352, 233, 327);
      ctx.bezierCurveTo(238, 320, 239, 311, 239, 301);
      ctx.lineTo(239, 216);
      ctx.lineTo(321, 197);
      ctx.lineTo(321, 271);
      ctx.bezierCurveTo(301, 258, 261, 269, 258, 298);
      ctx.bezierCurveTo(255, 325, 302, 335, 319, 310);
      ctx.bezierCurveTo(323, 303, 324, 294, 324, 284);
      ctx.lineTo(324, 157);
      ctx.closePath();
      ctx.fill();
    } else if (icon === "shield") {
      ctx.beginPath();
      ctx.moveTo(256, 144);
      ctx.lineTo(344, 177);
      ctx.lineTo(336, 258);
      ctx.quadraticCurveTo(330, 309, 256, 352);
      ctx.quadraticCurveTo(182, 309, 176, 258);
      ctx.lineTo(168, 177);
      ctx.closePath();
      ctx.stroke();
      ctx.lineWidth = 20;
      ctx.beginPath();
      ctx.moveTo(218, 245);
      ctx.lineTo(246, 273);
      ctx.lineTo(298, 216);
      ctx.stroke();
    } else if (icon === "folder") {
      ctx.beginPath();
      ctx.moveTo(145, 190);
      ctx.quadraticCurveTo(145, 170, 165, 170);
      ctx.lineTo(229, 170);
      ctx.lineTo(254, 197);
      ctx.lineTo(347, 197);
      ctx.quadraticCurveTo(368, 197, 368, 218);
      ctx.lineTo(368, 315);
      ctx.quadraticCurveTo(368, 337, 346, 337);
      ctx.lineTo(166, 337);
      ctx.quadraticCurveTo(145, 337, 145, 316);
      ctx.closePath();
      ctx.fill();
      ctx.beginPath();
      ctx.moveTo(145, 220);
      ctx.lineTo(368, 220);
      ctx.strokeStyle = "#e7b781";
      ctx.lineWidth = 10;
      ctx.stroke();
    }

    ctx.restore();
  }

  function drawIcon(canvas, icon, color) {
    const ctx = canvas.getContext("2d");
    const [highlight, face, side, bottom] = palettes[color];
    const size = canvas.width;
    const scale = size / 512;

    ctx.save();
    ctx.scale(scale, scale);
    ctx.clearRect(0, 0, 512, 512);

    roundedRect(ctx, 82, 91, 348, 348, 92);
    ctx.fillStyle = bottom;
    ctx.fill();
    roundedRect(ctx, 82, 78, 348, 348, 92);
    ctx.fillStyle = side;
    ctx.fill();
    roundedRect(ctx, 82, 62, 348, 348, 92);
    const gradient = ctx.createLinearGradient(118, 58, 380, 403);
    gradient.addColorStop(0, highlight);
    gradient.addColorStop(0.38, face);
    gradient.addColorStop(1, side);
    ctx.fillStyle = gradient;
    ctx.fill();

    roundedRect(ctx, 96, 76, 320, 319, 78);
    ctx.strokeStyle = "rgb(255 255 255 / 24%)";
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.save();
    roundedRect(ctx, 82, 62, 348, 348, 92);
    ctx.clip();
    const sheen = ctx.createLinearGradient(96, 62, 270, 247);
    sheen.addColorStop(0, "rgb(255 255 255 / 24%)");
    sheen.addColorStop(0.44, "rgb(255 255 255 / 5%)");
    sheen.addColorStop(1, "rgb(255 255 255 / 0%)");
    ctx.fillStyle = sheen;
    ctx.fillRect(82, 62, 348, 200);
    ctx.restore();

    drawGlyph(ctx, icon);
    ctx.restore();
  }

  function render() {
    drawIcon(mainCanvas, state.icon, state.color);
    selectedName.textContent = names[state.icon];
    iconGrid.querySelectorAll(".icon-option").forEach((button) => {
      const selected = button.dataset.icon === state.icon;
      button.classList.toggle("is-selected", selected);
      button.setAttribute("aria-pressed", String(selected));
      drawIcon(button.querySelector("canvas"), button.dataset.icon, state.color);
    });
  }

  iconGrid.addEventListener("click", (event) => {
    const button = event.target.closest(".icon-option");
    if (!button) return;
    state.icon = button.dataset.icon;
    downloadNote.textContent = "A 512 × 512 transparent PNG, ready to copy to your device.";
    render();
  });

  swatches.addEventListener("click", (event) => {
    const button = event.target.closest(".swatch");
    if (!button) return;
    state.color = button.dataset.color;
    swatches.querySelectorAll(".swatch").forEach((swatch) => {
      const selected = swatch === button;
      swatch.classList.toggle("is-selected", selected);
      swatch.setAttribute("aria-pressed", String(selected));
    });
    downloadNote.textContent = "A 512 × 512 transparent PNG, ready to copy to your device.";
    render();
  });

  downloadButton.addEventListener("click", () => {
    mainCanvas.toBlob((blob) => {
      if (!blob) {
        downloadNote.textContent = "This browser could not create the PNG. Try a current browser.";
        return;
      }
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `field-kit-${state.icon}.png`;
      link.click();
      window.setTimeout(() => URL.revokeObjectURL(url), 1000);
      downloadNote.textContent = `${names[state.icon]} icon downloaded as field-kit-${state.icon}.png`;
    }, "image/png");
  });

  render();
})();
