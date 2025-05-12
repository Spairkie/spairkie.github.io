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

  // Resume Modal Functions
function openResumeModal() {
  document.getElementById("resumeModal").style.display = "block";
}

function closeResumeModal() {
  document.getElementById("resumeModal").style.display = "none";
}

window.addEventListener("click", function(event) {
  const modal = document.getElementById("resumeModal");
  if (event.target === modal) {
    closeResumeModal();
  }
});

// Close modal on ESC key
document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape') {
    closeResumeModal();
  }
});