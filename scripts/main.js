window.addEventListener("load", () => {
  const preloader = document.getElementById("preloader");
  const screen = document.querySelector(".access-screen");
  const granted = document.querySelector(".access-granted");
  const spinner = document.querySelector(".neon-spinner");
  const line = document.querySelector(".access-line");
  const canvas = document.getElementById("matrixCanvas");
  const ctx = canvas.getContext("2d");

  // const hasSeenIntro = sessionStorage.getItem("seenIntro");
  const hasSeenIntro = localStorage.getItem("seenIntro") === "true";


  if (hasSeenIntro && preloader) {
    preloader.remove(); // Skip preloader entirely
    return;
  }

  // Unhide the preloader only if animation is needed
  // sessionStorage.setItem("seenIntro", "true");
  localStorage.setItem("seenIntro", "true");
  preloader.classList.remove("preloader-hidden");

  // Setup canvas
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&*".split("");
  const fontSize = 16;
  const columns = Math.floor(canvas.width / fontSize);
  const drops = Array(columns).fill(1);

  function drawMatrix() {
    ctx.fillStyle = "rgba(44, 62, 80, 0.08)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#00ff9f";
    ctx.font = fontSize + "px monospace";

    for (let i = 0; i < drops.length; i++) {
      const text = chars[Math.floor(Math.random() * chars.length)];
      ctx.fillText(text, i * fontSize, drops[i] * fontSize);
      if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
        drops[i] = 0;
      }
      drops[i]++;
    }

    requestAnimationFrame(drawMatrix);
  }

  // Preloader animation sequence
  setTimeout(() => {
    spinner.classList.add("hide");
    line.classList.add("hide");
  }, 2000);

  setTimeout(() => {
    granted.classList.add("show");
  }, 2500);

  setTimeout(() => {
    screen.classList.add("fade-out");
    canvas.classList.add("show");
    drawMatrix();
  }, 4000);

  setTimeout(() => {
    canvas.classList.remove("show");
    preloader.classList.add("fade-out");
    setTimeout(() => {
      preloader.remove();
      history.replaceState({}, document.title, window.location.pathname);
    }, 1200);
  }, 7000);
});
document.addEventListener("keydown", function (e) {
  const isCtrlR = (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "r";

  if (isCtrlR) {
    e.preventDefault(); // Stop default page reload
    localStorage.removeItem("seenIntro");
    location.reload(); // Triggers Matrix intro again
  }
});

// === Toggle Mobile Navigation ===
function toggleNav() {
  const navLinks = document.querySelector('.nav-links');
  const overlay = document.querySelector('.nav-overlay');
  const hamburger = document.querySelector('.hamburger');

  navLinks.classList.toggle('show');
  overlay.classList.toggle('show');
  hamburger.classList.toggle('open');
}

// Close mobile nav on link click (only on mobile)
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 768) {
        toggleNav();
      }
    });
  });
});

// === Sticky Navbar Scroll Effect ===
window.addEventListener('scroll', () => {
  const nav = document.querySelector('nav');
  if (window.scrollY > 10) {
    nav.classList.add('scrolled');
  } else {
    nav.classList.remove('scrolled');
  }
});

// === Highlight Active Nav Link Based on Scroll Position ===
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

// === Smooth Scroll for Anchor Links ===
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({
        behavior: 'smooth'
      });
    }
  });
});

// === Scroll to Top Button ===
const scrollTopBtn = document.getElementById("scrollTopBtn");

window.addEventListener("scroll", () => {
  const shouldShow = document.body.scrollTop > 300 || document.documentElement.scrollTop > 300;
  if (scrollTopBtn) {
    scrollTopBtn.style.display = shouldShow ? "block" : "none";
  }
});

if (scrollTopBtn) {
  scrollTopBtn.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  });
}

// === Animate About Section on Scroll ===
document.addEventListener("DOMContentLoaded", () => {
  const aboutSection = document.querySelector('#about');

  if (aboutSection) {
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in-right');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1
    });

    observer.observe(aboutSection);
  }
});

// === Project Carousel Logic ===
const carousel = document.getElementById('projectCarousel');
const dotsContainer = document.getElementById('carouselDots');
const itemCount = carousel?.children.length || 0;
const itemWidth = carousel?.children[0]?.offsetWidth + 20 || 0;
const visibleWidth = carousel?.offsetWidth || 0;
const itemsPerView = Math.floor(visibleWidth / itemWidth) || 1;
const dotCount = Math.ceil(itemCount / itemsPerView);
let autoScroll;
let activeIndex = 0;

function updateDots(index) {
  document.querySelectorAll('.carousel-dot').forEach((dot, i) => {
    dot.classList.toggle('active', i === index);
  });
}

function goToSlide(index) {
  if (!carousel) return;
  carousel.scrollTo({
    left: index * itemWidth * itemsPerView,
    behavior: 'smooth'
  });
  activeIndex = index;
  updateDots(index);
}

function scrollCarousel(direction) {
  if (!carousel) return;
  const scrollAmount = itemWidth * itemsPerView;
  carousel.scrollBy({
    left: direction * scrollAmount,
    behavior: 'smooth'
  });
  activeIndex += direction;
  activeIndex = Math.max(0, Math.min(activeIndex, dotCount - 1));
  updateDots(activeIndex);
}

function autoScrollCarousel() {
  autoScroll = setInterval(() => {
    if (!carousel) return;
    if (carousel.scrollLeft + carousel.clientWidth >= carousel.scrollWidth - 5) {
      carousel.scrollTo({
        left: 0,
        behavior: 'smooth'
      });
      activeIndex = 0;
    } else {
      scrollCarousel(1);
    }
    updateDots(activeIndex);
  }, 4000);
}

if (dotsContainer && itemCount > 0) {
  for (let i = 0; i < dotCount; i++) {
    const dot = document.createElement('span');
    dot.classList.add('carousel-dot');
    if (i === 0) dot.classList.add('active');
    dot.addEventListener('click', () => goToSlide(i));
    dotsContainer.appendChild(dot);
  }
}

if (carousel) {
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
    const moveX = e.touches[0].clientX;
    const diff = startX - moveX;
    if (Math.abs(diff) > 50) {
      scrollCarousel(diff > 0 ? 1 : -1);
      isDown = false;
    }
  });

  carousel.addEventListener('touchend', () => {
    isDown = false;
  });

  autoScrollCarousel();
}


// === Animate Timeline Entries and Resume CTA ===
document.addEventListener("DOMContentLoaded", () => {
  const timelineItems = document.querySelectorAll(".timeline-entry");
  const resumeCta = document.querySelector(".resume-cta");

  const observerOptions = {
    threshold: 0.15
  };

  const timelineObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add("visible"), index * 150);
      } else {
        entry.target.classList.remove("visible");
      }
    });
  }, observerOptions);

  timelineItems.forEach(item => timelineObserver.observe(item));

  if (resumeCta) {
    const ctaObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          setTimeout(() => entry.target.classList.add("visible"), timelineItems.length * 150);
        } else {
          entry.target.classList.remove("visible");
        }
      });
    }, observerOptions);

    ctaObserver.observe(resumeCta);
  }
});


// === Animate Skills Section and Tags on Scroll ===
document.addEventListener("DOMContentLoaded", () => {
  const skillsSection = document.getElementById("skills");
  const skillTags = document.querySelectorAll(".skill-tag");

  if (skillsSection) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          skillsSection.classList.add("visible");
          skillTags.forEach((tag, index) => {
            setTimeout(() => tag.classList.add("visible"), index * 70);
          });
        } else {
          skillsSection.classList.remove("visible");
          skillTags.forEach(tag => tag.classList.remove("visible"));
        }
      });
    }, {
      threshold: 0.1
    });

    observer.observe(skillsSection);
  }
});

// === Animate Education Section and Entries on Scroll ===
document.addEventListener("DOMContentLoaded", () => {
  const eduSection = document.getElementById("education");
  const eduEntries = document.querySelectorAll(".education-entry");

  if (eduSection) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          eduSection.classList.add("visible");
          eduEntries.forEach((entry, i) => {
            setTimeout(() => entry.classList.add("visible"), i * 150);
          });
        } else {
          eduSection.classList.remove("visible");
          eduEntries.forEach(entry => entry.classList.remove("visible"));
        }
      });
    }, {
      threshold: 0.1
    });

    observer.observe(eduSection);
  }
});

// === Certifications Carousel Logic ===
const certCarousel = document.getElementById('certCarousel');
const certLeftBtn = document.getElementById('certLeftBtn');
const certRightBtn = document.getElementById('certRightBtn');
const certDotsContainer = document.getElementById('certDots');
const certItemWidth = certCarousel?.children[0]?.offsetWidth + 20 || 0;
const certVisibleWidth = certCarousel?.offsetWidth || 0;
const certItemsPerView = Math.floor(certVisibleWidth / certItemWidth) || 1;
const certItemCount = certCarousel?.children.length || 0;
const certDotCount = Math.ceil(certItemCount / certItemsPerView);
let certAutoScroll;
let certActiveIndex = 0;

function updateCertDots(index) {
  document.querySelectorAll('.cert-dot').forEach((dot, i) => {
    dot.classList.toggle('active', i === index);
  });
}

function updateCertNavButtons() {
  const atLeft = certCarousel.scrollLeft <= 5;
  const atRight = certCarousel.scrollLeft + certCarousel.clientWidth >= certCarousel.scrollWidth - 5;
  certLeftBtn.classList.toggle('hidden', atLeft);
  certRightBtn.classList.toggle('hidden', atRight);
}

function goToCertSlide(index) {
  certCarousel.scrollTo({
    left: index * certItemWidth * certItemsPerView,
    behavior: 'smooth'
  });
  certActiveIndex = index;
  updateCertDots(index);
}

function scrollCertCarousel(direction) {
  const scrollAmount = certItemWidth * certItemsPerView;
  certCarousel.scrollBy({
    left: direction * scrollAmount,
    behavior: 'smooth'
  });
  certActiveIndex += direction;
  certActiveIndex = Math.max(0, Math.min(certActiveIndex, certDotCount - 1));
  updateCertDots(certActiveIndex);
  setTimeout(updateCertNavButtons, 400);
}

function autoScrollCertCarousel() {
  certAutoScroll = setInterval(() => {
    if (certCarousel.scrollLeft + certCarousel.clientWidth >= certCarousel.scrollWidth - 5) {
      certCarousel.scrollTo({
        left: 0,
        behavior: 'smooth'
      });
      certActiveIndex = 0;
    } else {
      scrollCertCarousel(1);
    }
    updateCertDots(certActiveIndex);
  }, 5000);
}

// Dot nav generation
if (certDotsContainer && certItemCount > 0) {
  for (let i = 0; i < certDotCount; i++) {
    const dot = document.createElement('span');
    dot.classList.add('cert-dot');
    if (i === 0) dot.classList.add('active');
    dot.addEventListener('click', () => goToCertSlide(i));
    certDotsContainer.appendChild(dot);
  }
}

// Event listeners
certLeftBtn?.addEventListener('click', () => scrollCertCarousel(-1));
certRightBtn?.addEventListener('click', () => scrollCertCarousel(1));
certCarousel?.addEventListener('mouseenter', () => clearInterval(certAutoScroll));
certCarousel?.addEventListener('mouseleave', autoScrollCertCarousel);
certCarousel?.addEventListener('scroll', updateCertNavButtons);

// Touch support
let certStartX = 0;
let certIsTouching = false;

certCarousel?.addEventListener('touchstart', (e) => {
  certStartX = e.touches[0].clientX;
  certIsTouching = true;
  clearInterval(certAutoScroll);
});

certCarousel?.addEventListener('touchmove', (e) => {
  if (!certIsTouching) return;
  const moveX = e.touches[0].clientX;
  const diff = certStartX - moveX;
  if (Math.abs(diff) > 50) {
    scrollCertCarousel(diff > 0 ? 1 : -1);
    certIsTouching = false;
  }
});

certCarousel?.addEventListener('touchend', () => {
  certIsTouching = false;
  autoScrollCertCarousel();
});

window.addEventListener('resize', updateCertNavButtons);
window.addEventListener('load', () => {
  updateCertNavButtons();
  autoScrollCertCarousel();
});

// Flip cards on click
document.querySelectorAll('.cert-card').forEach(card => {
  card.addEventListener('click', () => {
    card.classList.toggle('flipped');
  });
});

// === Resume Modal Logic ===
document.addEventListener("DOMContentLoaded", () => {
  const resumeModal = document.getElementById("resumeModal");
  const resumeCloseBtn = resumeModal?.querySelector(".close");

  window.openResumeModal = function() {
    if (resumeModal) {
      const iframe = document.getElementById("resumeIframe");
      if (iframe && !iframe.src) {
        iframe.src = iframe.dataset.src;
      }
      resumeModal.style.display = "block";
    }
  };


  window.closeResumeModal = function() {
    if (resumeModal) resumeModal.style.display = "none";
  };

  window.addEventListener("click", function(event) {
    if (event.target === resumeModal) {
      closeResumeModal();
    }
  });

  document.addEventListener("keydown", function(e) {
    if (e.key === "Escape" && resumeModal?.style.display === "block") {
      closeResumeModal();
    }
  });

  resumeCloseBtn?.addEventListener("click", closeResumeModal);
});

// === Contact Modal Logic ===
document.addEventListener("DOMContentLoaded", () => {
  const contactModal = document.getElementById("contactModal");
  const contactForm = document.getElementById("contactForm");
  const thankYou = document.getElementById("thankYouMsg");
  const contactCloseBtn = contactModal?.querySelector(".close");

  window.openContactModal = function() {
    if (contactModal) contactModal.style.display = "block";
  };

  window.closeContactModal = function() {
    if (contactModal) contactModal.style.display = "none";
  };

  window.addEventListener("click", function(event) {
    if (event.target === contactModal) {
      closeContactModal();
    }
  });

  document.addEventListener("keydown", function(e) {
    if (e.key === "Escape" && contactModal?.style.display === "block") {
      closeContactModal();
    }
  });

  contactCloseBtn?.addEventListener("click", closeContactModal);

  if (contactForm && thankYou) {
    contactForm.addEventListener("submit", function(e) {
      e.preventDefault();
      const formData = new FormData(contactForm);

      fetch(contactForm.action, {
          method: "POST",
          body: formData,
          headers: {
            Accept: "application/json"
          }
        })
        .then(response => {
          if (response.ok) {
            contactForm.style.display = "none";
            thankYou.style.display = "block";
          } else {
            alert("Oops! Something went wrong.");
          }
        })
        .catch(() => {
          alert("There was a problem submitting the form.");
        });
    });

    // Allow "Enter" key to submit form cleanly (without newline spam)
    document.addEventListener("keydown", function(event) {
      if (
        contactModal?.style.display === "block" &&
        event.key === "Enter" &&
        document.activeElement &&
        contactForm.contains(document.activeElement)
      ) {
        event.preventDefault();
        contactForm.requestSubmit();
      }
    });
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const shareBtn = document.getElementById("shareBtn");

  if (navigator.share) {
    shareBtn.style.display = "inline-flex"; // make visible only if supported
    shareBtn.addEventListener("click", (e) => {
      e.preventDefault();
      navigator
        .share({
          title: "Hans' Portfolio",
          text: "Check out this awesome portfolio!",
          url: window.location.href,
        })
        .then(() => console.log("Shared successfully!"))
        .catch((err) => console.error("Share failed:", err));
    });
  }

});

// === Terminal Interaction Logic ===

document.addEventListener("DOMContentLoaded", () => {
  const output = document.getElementById("terminalOutput");
  const input = document.getElementById("terminalInput");
  const cursor = document.getElementById("terminalCursor");
  const scrollRegion = document.getElementById("terminalScroll");

  const bootTime = Date.now();

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
    "date": [new Date().toString()],
    "help": [],
    "sudo make me a sandwich": ["Okay. 🥪", "(That worked?!)"],
    "echo hello, world!": ["Hello, World!"],
    "rm -rf /": [
      "Warning: this will delete EVERYTHING...",
      "Just kidding. 😅 You're safe here."
    ],
    "ascii hans": [
      " _   _              ____  ",
      "| | | | __ _ _ __ / ___| ",
      "| |_| |/ _` | '__\\___ \ ",
      "|  _  | (_| | |  |  ___)|",
      "|_| |_|\\__,_|_| |_|____/ ",
      "  H   A  N  S   S A I     "
    ],
    "uname -a": [
      "HansOS 1.0.5-elite x86_64 HansKernel SMP Wed May 2025",
      "Compiled for awesome people only"
    ],
    "neofetch": [
      "HansOS 1.0.5",
      "------------",
      "User: hans",
      "Shell: /bin/bash (emulated)",
      "Uptime: ∞",
      "Terminal: Web CLI",
      "Certs: Security+ | ITF+ | MTA",
      "Quote: \"Stay ready so you don’t have to get ready.\""
    ],
    "ping google.com": [
      "Pinging google.com [142.250.72.14] with 32 bytes of data:",
      "Reply from 142.250.72.14: bytes=32 time=42ms TTL=57",
      "Reply from 142.250.72.14: bytes=32 time=39ms TTL=57",
      "Reply from 142.250.72.14: bytes=32 time=40ms TTL=57",
      "",
      "Ping statistics for google.com:",
      "    Packets: Sent = 3, Received = 3, Lost = 0 (0% loss),",
      "Approximate round trip times in milliseconds:",
      "    Minimum = 39ms, Maximum = 42ms, Average = 40ms"
    ]
  };

  // Aliases
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

  responses["restart matrix"] = function() {
    localStorage.removeItem("seenIntro");
    location.reload();
    return ["Restarting Matrix..."];
  }
  
  responses["help"] = [
    "Available commands:",
    ...Object.keys(responses).filter(cmd => !["help", "clear"].includes(cmd)).map(cmd => `• ${cmd}`)
  ];

  // Dynamic: uptime
  responses["uptime"] = function() {
    const ms = Date.now() - bootTime;
    const h = Math.floor(ms / (1000 * 60 * 60));
    const m = Math.floor((ms / (1000 * 60)) % 60);
    const s = Math.floor((ms / 1000) % 60);
    return [`Uptime: ${h}h ${m}m ${s}s`];
  };

  // Dynamic: current time
  responses["date +%T"] = function() {
    const now = new Date();
    const time = now.toLocaleTimeString();
    return [`Current time: ${time}`];
  };

  
  responses["open bento"] = () => {
    return function() {
      printLine("Redirecting to Bento site...");
      window.location.href = "/bento.html";
      return Promise.resolve();
    };
  };


  responses["bento"] = responses["open bento"];
  responses["goto bento"] = responses["open bento"];



  function typeText(line, container, delay = 30, callback) {
    let i = 0;
    const div = document.createElement("div");
    container.appendChild(div);

    function typeChar() {
      if (i < line.length) {
        div.textContent += line.charAt(i);
        i++;
        scrollRegion.scrollTop = scrollRegion.scrollHeight;
        setTimeout(typeChar, delay);
      } else if (callback) callback();
    }
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
      } else if (callback) callback();
    }
    typeNext();
  }

  function bootSequence() {
    cursor.style.display = "none";
    typeLines(["> whoami"], 400, () => {
      typeLines(responses["whoami"], 400, () => {
        cursor.style.display = "inline-block";
        input.removeAttribute("disabled");
        input.focus();
      });
    });
  }

  bootSequence();

  input.addEventListener("keydown", e => {
    if (e.key === "Enter") {
      const command = input.value.trim().toLowerCase();
      const prompt = document.createElement("div");
      prompt.textContent = `> ${command}`;
      output.appendChild(prompt);

      input.value = "";
      cursor.style.display = "none";

      if (command === "clear") {
        output.innerHTML = "";
        cursor.style.display = "inline-block";
        return;
      }



      if (responses.hasOwnProperty(command)) {
        const res = responses[command];
        if (typeof res === "function") {
          const result = res(command);
          if (result instanceof Promise) {
            result.then(lines => typeLines(lines, 300, () => cursor.style.display = "inline-block"));
          } else {
            typeLines([result].flat(), 300, () => cursor.style.display = "inline-block");
          }
        } else {
          typeLines(res, 300, () => cursor.style.display = "inline-block");
        }
      } else {
        typeLines([
          `Command not found: ${command}`,
          "Try commands like: whoami, skills, ascii hans, uptime, or help."
        ], 300, () => cursor.style.display = "inline-block");
      }
    }
  });

  input.addEventListener("input", () => {
    cursor.classList.add("typing");
    const span = document.createElement("span");
    span.style.visibility = "hidden";
    span.style.position = "absolute";
    span.style.font = getComputedStyle(input).font;
    span.textContent = input.value || input.placeholder || "";
    document.body.appendChild(span);
    input.style.width = `${Math.min(span.offsetWidth + 10, 300)}px`;
    document.body.removeChild(span);
  });

  ["blur", "focusout"].forEach(event => input.addEventListener(event, () => {
    cursor.classList.remove("typing");
  }));

  input.addEventListener("keyup", e => {
    if (e.key !== "Enter") {
      setTimeout(() => cursor.classList.remove("typing"), 500);
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const scrollBtn = document.getElementById("scrollTopBtn");
  const installText = document.getElementById("installText");
  const scrollIcon = scrollBtn.querySelector("svg");
  let deferredPrompt = null;

  // Scroll to top on logo click
  const logo = document.querySelector(".nav-logo");
  if (logo) {
    logo.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // Catch install event
  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredPrompt = e;
    maybeShowInstall();
  });

  // Button click handler
  scrollBtn.addEventListener("click", () => {
    if (installText.style.display === "inline" && deferredPrompt) {
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then((choice) => {
        if (choice.outcome === "accepted") {
          console.log("User installed the app");
        }
        deferredPrompt = null;
        hideInstallPrompt();
      });
    } else {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  });

  // Scroll event toggle
  window.addEventListener("scroll", () => {
    if (window.scrollY < 20 && deferredPrompt) {
      showInstallPrompt();
    } else if (window.scrollY > 100) {
      showScrollButton();
    } else {
      hideInstallPrompt();
    }
  });

  function maybeShowInstall() {
    if (window.scrollY < 20 && deferredPrompt) {
      showInstallPrompt();
    }
  }

  function showInstallPrompt() {
    scrollBtn.classList.add("fade-in");
    scrollBtn.classList.remove("fade-out");
    scrollBtn.style.display = "flex";
    installText.style.display = "inline";
    scrollIcon.style.display = "none";
  }

  function showScrollButton() {
    scrollBtn.classList.add("fade-in");
    scrollBtn.classList.remove("fade-out");
    scrollBtn.style.display = "flex";
    installText.style.display = "none";
    scrollIcon.style.display = "inline";
  }

  function hideInstallPrompt() {
    scrollBtn.classList.add("fade-out");
    scrollBtn.classList.remove("fade-in");
    // Optionally: scrollBtn.style.display = "none"; after animation ends
  }

  // Fallback check (e.g. if no scroll occurs)
  setTimeout(() => {
    maybeShowInstall();
  }, 1000);
});

document.addEventListener("DOMContentLoaded", () => {
  if ('loading' in HTMLImageElement.prototype) return; // native lazy loading is supported

  const lazyImages = document.querySelectorAll('img[loading="lazy"]');
  lazyImages.forEach(img => {
    const src = img.getAttribute('src');
    if (src) {
      img.src = src;
    }
  });
});


if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/scripts/sw.js")
      .then(reg => console.log("Service Worker registered:", reg.scope))
      .catch(err => console.error("Service Worker registration failed:", err));
  });
}