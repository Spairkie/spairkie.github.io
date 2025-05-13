// Make logo clickable to scroll to top/home
  document.addEventListener('DOMContentLoaded', () => {
    const logo = document.querySelector('.nav-logo');
    if (logo) {
      logo.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }
  });// === Toggle Mobile Nav ===
function toggleNav() {
  const navLinks = document.querySelector('.nav-links');
  const overlay = document.querySelector('.nav-overlay');
  const hamburger = document.querySelector('.hamburger');
  navLinks.classList.toggle('show');
  overlay.classList.toggle('show');
  hamburger.classList.toggle('open');
}
window.addEventListener('scroll', () => {
  const nav = document.querySelector('nav');
  if (window.scrollY > 10) {
    nav.classList.add('scrolled');
  } else {
    nav.classList.remove('scrolled');
  }
});


document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    if (window.innerWidth <= 768) {
      toggleNav();
    }
  });
});

// === Scroll to Top Button ===
const scrollTopBtn = document.getElementById("scrollTopBtn");

window.onscroll = function () {
  if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
    scrollTopBtn.style.display = "block";
  } else {
    scrollTopBtn.style.display = "none";
  }
};

scrollTopBtn.addEventListener("click", function () {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

// === jQuery Slick Carousel ===
$(document).ready(function() {
  $('.carousel').slick({
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    adaptiveHeight: true
  });
});

// === Project Carousel ===
const carousel = document.getElementById('projectCarousel');
const dotsContainer = document.getElementById('carouselDots');
const itemCount = carousel.children.length;
const itemWidth = carousel.children[0].offsetWidth + 20;
const visibleWidth = carousel.offsetWidth;
const itemsPerView = Math.floor(visibleWidth / itemWidth);
const dotCount = Math.ceil(itemCount / itemsPerView);
let autoScroll;
let activeIndex = 0;

function scrollCarousel(direction) {
  const scrollAmount = itemWidth * itemsPerView;
  carousel.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
  updateDots(direction);
}

function autoScrollCarousel() {
  autoScroll = setInterval(() => {
    if (carousel.scrollLeft + carousel.clientWidth >= carousel.scrollWidth) {
      carousel.scrollTo({ left: 0, behavior: 'smooth' });
      activeIndex = 0;
      updateDots(0);
    } else {
      scrollCarousel(1);
    }
  }, 4000);
}

function updateDots(direction) {
  activeIndex += direction;
  if (activeIndex < 0) activeIndex = 0;
  if (activeIndex >= dotCount) activeIndex = dotCount - 1;

  document.querySelectorAll('.carousel-dot').forEach((dot, i) => {
    dot.classList.toggle('active', i === activeIndex);
  });
}

function goToSlide(index) {
  carousel.scrollTo({ left: index * itemWidth * itemsPerView, behavior: 'smooth' });
  activeIndex = index;
  updateDots(0);
}

for (let i = 0; i < dotCount; i++) {
  const dot = document.createElement('span');
  dot.classList.add('carousel-dot');
  if (i === 0) dot.classList.add('active');
  dot.addEventListener('click', () => goToSlide(i));
  dotsContainer.appendChild(dot);
}

carousel.addEventListener('mouseenter', () => clearInterval(autoScroll));
carousel.addEventListener('mouseleave', autoScrollCarousel);

let startX = 0;
let isDown = false;

carousel.addEventListener('touchstart', (e) => {
  startX = e.touches[0].clientX;
  isDown = true;
});

carousel.addEventListener('touchmove', (e) => {
  if (!isDown) return;
  let moveX = e.touches[0].clientX;
  let diff = startX - moveX;
  if (Math.abs(diff) > 50) {
    scrollCarousel(diff > 0 ? 1 : -1);
    isDown = false;
  }
});

carousel.addEventListener('touchend', () => {
  isDown = false;
});

autoScrollCarousel();

// === Certification Carousel ===
const certCarousel = document.getElementById('certCarousel');
const certLeftBtn = document.getElementById('certLeftBtn');
const certRightBtn = document.getElementById('certRightBtn');
const certDotsContainer = document.getElementById('certDots');
const certItemWidth = certCarousel.children[0].offsetWidth + 20;
const certVisibleWidth = certCarousel.offsetWidth;
const certItemsPerView = Math.floor(certVisibleWidth / certItemWidth);
const certItemCount = certCarousel.children.length;
const certDotCount = Math.ceil(certItemCount / certItemsPerView);
let certAutoScroll;
let certActiveIndex = 0;

function updateCertNavButtons() {
  const atLeft = certCarousel.scrollLeft <= 5;
  const atRight = certCarousel.scrollLeft + certCarousel.clientWidth >= certCarousel.scrollWidth - 5;
  certLeftBtn.classList.toggle('hidden', atLeft);
  certRightBtn.classList.toggle('hidden', atRight);
}

function updateCertDots(index) {
  document.querySelectorAll('.cert-dot').forEach((dot, i) => {
    dot.classList.toggle('active', i === index);
  });
}

function goToCertSlide(index) {
  certCarousel.scrollTo({ left: index * certItemWidth * certItemsPerView, behavior: 'smooth' });
  certActiveIndex = index;
  updateCertDots(index);
}

function scrollCertCarousel(direction) {
  const scrollAmount = certItemWidth * certItemsPerView;
  certCarousel.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
  certActiveIndex += direction;
  if (certActiveIndex < 0) certActiveIndex = 0;
  if (certActiveIndex >= certDotCount) certActiveIndex = certDotCount - 1;
  updateCertDots(certActiveIndex);
  setTimeout(updateCertNavButtons, 500);
}

function autoScrollCertCarousel() {
  certAutoScroll = setInterval(() => {
    if (certCarousel.scrollLeft + certCarousel.clientWidth >= certCarousel.scrollWidth - 5) {
      certCarousel.scrollTo({ left: 0, behavior: 'smooth' });
      certActiveIndex = 0;
      updateCertDots(0);
    } else {
      scrollCertCarousel(1);
    }
  }, 5000);
}

for (let i = 0; i < certDotCount; i++) {
  const dot = document.createElement('span');
  dot.classList.add('cert-dot');
  if (i === 0) dot.classList.add('active');
  dot.addEventListener('click', () => goToCertSlide(i));
  certDotsContainer.appendChild(dot);
}

certLeftBtn.addEventListener('click', () => scrollCertCarousel(-1));
certRightBtn.addEventListener('click', () => scrollCertCarousel(1));

certCarousel.addEventListener('mouseenter', () => clearInterval(certAutoScroll));
certCarousel.addEventListener('mouseleave', autoScrollCertCarousel);
certCarousel.addEventListener('scroll', updateCertNavButtons);

let certStartX = 0;
let certIsTouching = false;

certCarousel.addEventListener('touchstart', (e) => {
  certStartX = e.touches[0].clientX;
  certIsTouching = true;
  clearInterval(certAutoScroll);
});

certCarousel.addEventListener('touchmove', (e) => {
  if (!certIsTouching) return;
  const moveX = e.touches[0].clientX;
  const diff = certStartX - moveX;
  if (Math.abs(diff) > 50) {
    scrollCertCarousel(diff > 0 ? 1 : -1);
    certIsTouching = false;
  }
});

certCarousel.addEventListener('touchend', () => {
  certIsTouching = false;
  autoScrollCertCarousel();
});

window.addEventListener('resize', updateCertNavButtons);
window.addEventListener('load', () => {
  updateCertNavButtons();
  autoScrollCertCarousel();
});


const timelineEntries = document.querySelectorAll('.timeline-entry');

  const animateOnScroll = () => {
    timelineEntries.forEach(entry => {
      const rect = entry.getBoundingClientRect();
      if (rect.top < window.innerHeight - 100) {
        entry.classList.add('visible');
      }
    });
  };

  window.addEventListener('scroll', animateOnScroll);
  window.addEventListener('load', animateOnScroll);

window.addEventListener("scroll", () => {
  const sections = document.querySelectorAll("section");
  const navLinks = document.querySelectorAll(".nav-links a");
  let currentSectionId = "";

  sections.forEach((section) => {
    const rect = section.getBoundingClientRect();
    if (rect.top <= 120 && rect.bottom >= 120) {
      currentSectionId = section.id;
    }
  });

  navLinks.forEach((link) => {
    link.classList.remove("active");
    if (link.getAttribute("href") === `#${currentSectionId}`) {
      link.classList.add("active");
    }
  });
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({
        behavior: 'smooth'
      });
    }
  });
});

function openModal(id) {
  document.getElementById(id).style.display = "block";
}

function closeModal(id) {
  document.getElementById(id).style.display = "none";
}

window.onclick = function(event) {
  document.querySelectorAll('.modal').forEach(modal => {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
};

function openContactModal() {
  openModal('contactModal');
}

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal').forEach(modal => {
      if (modal.style.display === 'block') {
        modal.style.display = 'none';
      }
    });
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const output = document.getElementById("terminalOutput");
  const input = document.getElementById("terminalInput");
  const cursor = document.getElementById("terminalCursor");

  const responses = {
    "whoami": [
      "Hi, I'm Hans",
      "IT Support Specialist",
      "Air Force Reservist",
      "Cybersecurity Student"
    ],
    "sudo": ["Permission denied. You are not in the sudoers file."],
    "skills": [
      "✔ Active Directory  ✔ PXE Boot  ✔ SmartDeploy",
      "✔ PowerShell  ✔ Security+  ✔ ITSM / ITOM / HRSD"
    ],
    "ls projects": [ 
      "📁 Helpdesk Ticketing System",
      "📁 Bash Resource Monitor",
      "📁 React Chat App"
    ],
    "cd about": [
      "Navigating to /about/",
      "Hans Sai is an IT specialist with experience in both military and civilian systems..."
    ],
    "cat education": [
      "Liberty University – BS in Computer Science (Cybersecurity)",
      "CCAF A.A.S. – Health Info Tech & Services"
    ],
    "ls certs": [
      "📜 CompTIA Security+",
      "📜 CompTIA IT Fundamentals+",
      "📜 Microsoft OS Fundamentals",
      "📜 Six Sigma Green Belt"
    ],
    "cat resume": [
      "Opening resume modal...",
      "(Not really, but you can click the resume button!)"
    ],
    "clear": [],

    // NEW: Current system date
    "date": [new Date().toString()],

    // NEW: Dynamic command list
    "help": [], // will be set dynamically below
  };

  // Multi-mapping (aliases)
  responses["projects"] = responses["ls projects"];
  responses["certs"] = responses["ls certs"];
  responses["education"] = responses["cat education"];
  responses["resume"] = responses["cat resume"];
  responses["motd"] = [
    "==============================",
    "   Welcome to Hans Terminal",
    "==============================",
    "💡 IT Specialist | Cybersecurity Student",
    "🛡️  CompTIA Security+ | Active Directory | PowerShell",
    "",
    "\"Discipline is the bridge between goals and accomplishment.\""
  ];

  // Help command auto-generates list
  responses["help"] = [
    "Available commands:",
    ...Object.keys(responses).filter(cmd => !["help", "clear"].includes(cmd)).map(cmd => `• ${cmd}`)
  ];
  responses["sudo make me a sandwich"] = [
    "Okay. 🥪",
    "(That worked?!)"
  ];

  responses["echo hello, world!"] = [
    "Hello, World!"
  ];

  responses["rm -rf /"] = [
    "Warning: this will delete EVERYTHING...",
    "Just kidding. 😅 You're safe here."
  ];

responses["ascii hans"] = [
  " _   _              ____  ",
  "| | | | __ _ _ __ / ___| ",
  "| |_| |/ _` | '__\\\___ \ ",
  "|  _  | (_| | |  |  ___)|",
  "|_| |_|\\__,_|_| |_|____/ ",
  "  H   A   N   S   S A I "
];


responses["uname -a"] = [
  "HansOS 1.0.5-elite x86_64 HansKernel SMP Wed May 2025",
  "Compiled for awesome people only"
];
responses["neofetch"] = [
  "HansOS 1.0.5",
  "------------",
  "User: hans",
  "Shell: /bin/bash (emulated)",
  "Uptime: ∞",
  "Terminal: Web CLI",
  "Certs: Security+ | ITF+ | MTA",
  "Quote: \"Stay ready so you don’t have to get ready.\""
];

responses["ping google.com"] = [
  "Pinging google.com [142.250.72.14] with 32 bytes of data:",
  "Reply from 142.250.72.14: bytes=32 time=42ms TTL=57",
  "Reply from 142.250.72.14: bytes=32 time=39ms TTL=57",
  "Reply from 142.250.72.14: bytes=32 time=40ms TTL=57",
  "",
  "Ping statistics for google.com:",
  "    Packets: Sent = 3, Received = 3, Lost = 0 (0% loss),",
  "Approximate round trip times in milliseconds:",
  "    Minimum = 39ms, Maximum = 42ms, Average = 40ms"
];



  function typeText(line, container, delay = 30, callback) {
    let charIndex = 0;
    const div = document.createElement("div");

    function typeChar() {
      if (charIndex < line.length) {
        div.textContent += line.charAt(charIndex);
        charIndex++;
        setTimeout(typeChar, delay);
      } else {
        if (callback) callback();
      }
    }

    container.appendChild(div);
    typeChar();
  }

  function typeLines(lines, delayBetween = 300, callback) {
    let i = 0;
    function typeNext() {
      if (i < lines.length) {
        typeText(lines[i], output, 30, () => {
          i++;
          setTimeout(typeNext, delayBetween);
        });
      } else if (callback) {
        callback();
      }
    }
    typeNext();
  }

  // Initial animated boot: whoami + response
  function bootSequence() {
    cursor.style.display = "none";
    typeLines(
      ["> whoami"],
      400,
      () => {
        typeLines(responses["whoami"], 400, () => {
          cursor.style.display = "inline-block";
          input.removeAttribute("disabled");
          input.focus();
        });
      }
    );
  }

  bootSequence();

  // Handle user input
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      const command = input.value.trim().toLowerCase();
      const prompt = document.createElement("div");
      prompt.textContent = `> ${command}`;
      output.appendChild(prompt);

      if (command === "clear") {
        output.innerHTML = "";
        cursor.style.display = "none";
      } else if (responses.hasOwnProperty(command)) {
        cursor.style.display = "none";
        typeLines(responses[command], 300, () => {
          cursor.style.display = "inline-block";
        });
      } else {
        cursor.style.display = "none";
        typeLines([
          `Command not found: ${command}`,
          "Try commands like: whoami, skills, ls projects, cat education, cat resume, or type help to see all options."
        ], 300, () => {
          cursor.style.display = "inline-block";
        });
      }

      input.value = "";
    }
  });
  // Cursor animation toggle while typing
input.addEventListener("input", () => {
  cursor.classList.add("typing");
});

input.addEventListener("blur", () => {
  cursor.classList.remove("typing");
});

input.addEventListener("focusout", () => {
  cursor.classList.remove("typing");
});

input.addEventListener("keyup", (e) => {
  if (e.key !== "Enter") {
    // Remove the typing class a bit after typing stops
    setTimeout(() => {
      cursor.classList.remove("typing");
    }, 500);
  }
});

});
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('terminalInput');

  function resizeInput() {
    const span = document.createElement('span');
    span.style.visibility = 'hidden';
    span.style.position = 'absolute';
    span.style.font = getComputedStyle(input).font;
    span.textContent = input.value || input.placeholder || '';
    document.body.appendChild(span);

    // Add a little extra space
    const width = Math.min(span.offsetWidth + 10, 300);
    input.style.width = `${width}px`;

    document.body.removeChild(span);
  }

  input.addEventListener('input', resizeInput);
  resizeInput(); // initialize on load
});

function typeText(line, container, delay = 30, callback) {
  let charIndex = 0;
  const div = document.createElement("div");
  const scrollRegion = document.getElementById("terminalScroll");

  function typeChar() {
    if (charIndex < line.length) {
      div.textContent += line.charAt(charIndex);
      charIndex++;
      scrollRegion.scrollTop = scrollRegion.scrollHeight; // force scroll down
      setTimeout(typeChar, delay);
    } else {
      if (callback) callback();
    }
  }

  container.appendChild(div);
  scrollRegion.scrollTop = scrollRegion.scrollHeight; // initial scroll
  typeChar();
}
