// Highlight active section in navigation
function highlightNavigation() {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('nav a');
    
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
  document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', function(e) {
      if (this.hash) {
        e.preventDefault();
        
        // Remove active class from all links
        document.querySelectorAll('nav a').forEach(l => {
          l.classList.remove('active');
        });
        
        // Add active class to clicked link
        this.classList.add('active');
        
        document.querySelector(this.hash).scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
  
  // Initialize navigation highlighting when page loads
  document.addEventListener('DOMContentLoaded', function() {
    highlightNavigation();
    
    // Set home as active by default
    const homeLink = document.querySelector('nav a[href="#hero"]');
    if (homeLink) {
      homeLink.classList.add('active');
    }
  });

document.getElementById('contactForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formStatus = document.getElementById('formStatus');
    const submitButton = this.querySelector('button[type="submit"]');
    
    // Get form data
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        message: document.getElementById('message').value
    };
    
    try {
        // Disable submit button
        submitButton.disabled = true;
        submitButton.textContent = 'Sending...';
        
        // Send data to backend
        const response = await fetch('http://localhost:5000/send-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Show success message
            formStatus.textContent = 'Message sent successfully!';
            formStatus.className = 'form-status success';
            
            // Reset form
            this.reset();
        } else {
            throw new Error(data.message || 'Failed to send message');
        }
    } catch (error) {
        // Show error message
        formStatus.textContent = error.message || 'Failed to send message. Please try again.';
        formStatus.className = 'form-status error';
    } finally {
        // Re-enable submit button
        submitButton.disabled = false;
        submitButton.textContent = 'Send Message';
    }
});