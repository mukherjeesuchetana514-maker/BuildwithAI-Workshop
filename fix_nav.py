import os
import glob
import re

new_nav = """    <!-- Navigation -->
    <nav class="fixed w-full z-50 glassmorphism transition-all duration-300">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-20">
                <div class="flex-shrink-0 flex items-center overflow-hidden">
                    <span class="font-bold text-lg sm:text-xl md:text-2xl tracking-widest uppercase truncate"><a href="/">MUKHERJEE FURNITURE</a></span>
                </div>
                <div class="hidden md:flex space-x-8 items-center">
                    <a href="/#collections" class="text-gray-800 hover:text-black transition-colors duration-200 text-sm font-medium tracking-wide uppercase">Collections</a>
                    <a href="/about" class="text-gray-800 hover:text-black transition-colors duration-200 text-sm font-medium tracking-wide uppercase">About</a>
                    <a href="/contact" class="text-gray-800 hover:text-black transition-colors duration-200 text-sm font-medium tracking-wide uppercase">Contact Us</a>
                    <a href="/cart" class="text-gray-800 hover:text-black transition-colors duration-200 text-sm font-medium tracking-wide uppercase">Cart</a>
                </div>
                <!-- Mobile menu button -->
                <button id="mobile-menu-btn" class="block md:hidden text-gray-800 hover:text-black focus:outline-none">
                    <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                </button>
            </div>
        </div>
    </nav>
    
    <!-- Mobile Menu Overlay -->
    <div id="mobile-menu-overlay" class="fixed inset-0 bg-black bg-opacity-50 z-[60] hidden transition-opacity duration-300 opacity-0"></div>
    
    <!-- Mobile Side Menu -->
    <div id="mobile-side-menu" class="fixed top-0 right-0 h-full w-64 bg-white shadow-2xl z-[70] transform translate-x-full transition-transform duration-300 ease-in-out flex flex-col">
        <div class="p-5 flex justify-end border-b border-gray-100">
            <button id="close-menu-btn" class="text-gray-800 hover:text-black focus:outline-none p-2 rounded-full hover:bg-gray-100 transition-colors">
                <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
        <div class="px-4 py-6 space-y-2 flex-grow">
            <a href="/#collections" class="block px-4 py-3 rounded-xl text-base font-medium text-gray-800 hover:text-white hover:bg-black uppercase tracking-wide transition-colors duration-200">Collections</a>
            <a href="/about" class="block px-4 py-3 rounded-xl text-base font-medium text-gray-800 hover:text-white hover:bg-black uppercase tracking-wide transition-colors duration-200">About</a>
            <a href="/contact" class="block px-4 py-3 rounded-xl text-base font-medium text-gray-800 hover:text-white hover:bg-black uppercase tracking-wide transition-colors duration-200">Contact Us</a>
            <a href="/cart" class="block px-4 py-3 rounded-xl text-base font-medium text-gray-800 hover:text-white hover:bg-black uppercase tracking-wide transition-colors duration-200">Cart</a>
        </div>
        <div class="p-6 border-t border-gray-100">
            <p class="text-xs text-gray-500 uppercase tracking-widest text-center">Mukherjee Furniture</p>
        </div>
    </div>"""

new_script = """    <!-- Script for Mobile Menu -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const btn = document.getElementById('mobile-menu-btn');
            const closeBtn = document.getElementById('close-menu-btn');
            const sideMenu = document.getElementById('mobile-side-menu');
            const overlay = document.getElementById('mobile-menu-overlay');

            function openMenu() {
                if(overlay && sideMenu) {
                    overlay.classList.remove('hidden');
                    void overlay.offsetWidth; // trigger reflow
                    overlay.classList.remove('opacity-0');
                    sideMenu.classList.remove('translate-x-full');
                }
            }

            function closeMenu() {
                if(overlay && sideMenu) {
                    overlay.classList.add('opacity-0');
                    sideMenu.classList.add('translate-x-full');
                    setTimeout(() => {
                        overlay.classList.add('hidden');
                    }, 300);
                }
            }

            if (btn && closeBtn && sideMenu && overlay) {
                btn.addEventListener('click', openMenu);
                closeBtn.addEventListener('click', closeMenu);
                overlay.addEventListener('click', closeMenu);
            }
        });
    </script>"""

nav_pattern = re.compile(r'<!-- Navigation -->.*?</nav>', re.DOTALL)
script_pattern = re.compile(r'<!-- Script for Mobile Menu -->.*?</script>', re.DOTALL)

for filepath in glob.glob("frontend/*.html"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<!-- Navigation -->' in content:
        content = nav_pattern.sub(new_nav, content)
        
    if '<!-- Script for Mobile Menu -->' in content:
        content = script_pattern.sub(new_script, content)
    else:
        # If it doesn't have the script, insert it before </body>
        if '</body>' in content:
            content = content.replace('</body>', new_script + '\n</body>')
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Updated all HTML files.")
