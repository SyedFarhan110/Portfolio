// Highlight active section in navigation
function highlightNavigation() {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    // Determine which section is currently in view
    window.addEventListener('scroll', function() {
      let current = '';
      sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if(pageYOffset >= (sectionTop - 150)) {
          current = section.getAttribute('id');
        }
      });
      
      // Update navigation highlighting
      navLinks.forEach(link => {
        link.classList.remove('active');
        if(link.getAttribute('href').slice(1) === current) {
          link.classList.add('active');
        }
      });
    });
  }
  
  // Smooth scroll for navigation
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href !== '#' && href.length > 1) {
        e.preventDefault();
        
        // Remove active class from all links
        document.querySelectorAll('.nav-menu a').forEach(l => {
          l.classList.remove('active');
        });
        
        // Add active class to clicked link
        if(this.classList.contains('nav-menu')) {
          this.classList.add('active');
        }
        
        const target = document.querySelector(href);
        if(target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });
  
  // Mobile menu toggle
  const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  const navMenu = document.querySelector('.nav-menu');
  
  if(mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', function() {
      navMenu.classList.toggle('active');
      this.querySelector('i').classList.toggle('fa-bars');
      this.querySelector('i').classList.toggle('fa-times');
    });
  }
  
  // Initialize navigation highlighting when page loads
  document.addEventListener('DOMContentLoaded', function() {
    highlightNavigation();
    
    // Set home as active by default
    const homeLink = document.querySelector('.nav-menu a[href="#hero"]');
    if (homeLink) {
      homeLink.classList.add('active');
    }
    
    // Add animation on scroll
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(entry => {
        if(entry.isIntersecting) {
          entry.target.style.animation = 'fadeInUp 0.6s ease-out';
          entry.target.style.opacity = '1';
        }
      });
    }, observerOptions);
    
    // Observe all cards
    document.querySelectorAll('.modern-project-card, .skill-category, .achievement-card, .timeline-item').forEach(el => {
      el.style.opacity = '0';
      observer.observe(el);
    });
  });

document.getElementById('contactForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formStatus = document.getElementById('formStatus');
    const submitButton = this.querySelector('button[type="submit"]');
    
    // Get form data
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;
    
    // Create FormData object
    const formData = new FormData();
    formData.append('name', name);
    formData.append('email', email);
    formData.append('message', `Subject: ${subject}\n\n${message}`);
    
    try {
        // Disable submit button
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        
        // Send data to backend
        const response = await fetch('http://127.0.0.1:8000/send-email', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Show success message
            formStatus.textContent = 'Message sent successfully! I\'ll get back to you soon.';
            formStatus.className = 'form-status success';
            
            // Reset form
            this.reset();
        } else {
            throw new Error(data.detail || 'Failed to send message');
        }
    } catch (error) {
        console.error('Error:', error);
        // Show error message
        formStatus.textContent = error.message || 'Failed to send message. Please try again or email me directly.';
        formStatus.className = 'form-status error';
    } finally {
        // Re-enable submit button
        submitButton.disabled = false;
        submitButton.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
        
        // Hide status message after 5 seconds
        setTimeout(() => {
            formStatus.style.display = 'none';
        }, 5000);
    }
});