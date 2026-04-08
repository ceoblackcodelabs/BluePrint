# views.py
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Quote, Service
from .forms import QuoteModelForm

class HomeView(TemplateView):
    template_name = 'Home/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QuoteModelForm()
        
        # Service data for display
        context['services'] = [
            {
                'name': 'Audio Systems',
                'slug': 'audio-systems',
                'icon': 'fas fa-volume-up',
                'tagline': 'Crystal Clear Sound for Every Moment',
                'image': 'images/audio-systems.jpg',
                'image_large': 'images/audio-systems.jpg',
                'full_description': 'At BluePrint AV, we understand that exceptional sound is the backbone of any successful event. Our professional audio systems deliver crystal-clear, powerful sound that captivates audiences and ensures every word, note, and beat is heard with precision. We utilize industry-leading equipment from renowned brands like L-Acoustics, d&b audiotechnik, and Shure to provide unparalleled audio quality for events of all sizes.\n\nFrom intimate corporate meetings to large-scale music festivals, our team of certified audio engineers designs custom sound solutions tailored to your venue\'s unique acoustics. We conduct thorough site assessments to determine optimal speaker placement, ensure even coverage, and eliminate dead spots. Our inventory includes line array systems, stage monitors, wireless microphones, digital mixing consoles, and in-ear monitoring systems.\n\nWhat sets us apart is our commitment to excellence at every stage. We provide on-site sound engineering throughout your event, making real-time adjustments to maintain perfect audio balance. Whether you need a simple PA system for a conference or a complex multi-zone setup for a festival, we deliver flawless sound that creates lasting memories.',
                'features': [
                    'Line Array Systems for even coverage',
                    'Wireless Microphones for freedom of movement',
                    'Stage Monitors for performers',
                    'Digital Mixing with recallable presets',
                    '24/7 On-site Technical Support',
                    'Custom Sound Calibration per venue'
                ],
                'technologies': ['L-Acoustics', 'd&b audiotechnik', 'Shure', 'Sennheiser', 'DiGiCo', 'Yamaha'],
                'industries': ['Concerts', 'Corporate Events', 'Weddings', 'Conferences', 'Festivals', 'Churches'],
                'experience_years': 12,
                'projects_completed': 450,
                'happy_clients': 380
            },
            {
                'name': 'Visual Displays',
                'slug': 'visual-displays',
                'icon': 'fas fa-tv',
                'tagline': 'Captivate Your Audience with Stunning Visuals',
                'image': 'images/visual-displays.jpg',
                'image_large': 'images/visual-displays.jpg',
                'full_description': 'Transform your event into a visual masterpiece with BluePrint AV\'s cutting-edge display solutions. We specialize in high-resolution LED walls, projection mapping, and immersive visual experiences that leave lasting impressions. Our inventory includes indoor and outdoor LED panels with pixel pitches ranging from P2.5 to P10, ensuring the perfect resolution for any viewing distance.\n\nOur team of visual design experts works closely with you to create custom content that aligns with your brand and event theme. From corporate presentations to concert visuals, we handle everything from content creation to seamless playback. Our 4K video processors ensure smooth, flicker-free imagery that looks spectacular on camera and in person.\n\nWe also offer creative services including video production, motion graphics, and real-time visual mixing. Whether you need a simple projection screen for a boardroom or a massive curved LED wall for a stadium concert, our technical team ensures flawless installation and operation throughout your event.',
                'features': [
                    'Indoor/Outdoor LED Walls',
                    'Projection Mapping Technology',
                    '4K Video Processing',
                    'Custom Content Creation',
                    'Curved and Custom-shaped Screens',
                    'Live Video Switching'
                ],
                'technologies': ['ROE Visual', 'Absen', 'Christie', 'Barco', 'Watchout', 'Resolume'],
                'industries': ['Concerts', 'Corporate Events', 'Product Launches', 'Trade Shows', 'Broadcast', 'Museums'],
                'experience_years': 10,
                'projects_completed': 320,
                'happy_clients': 290
            },
            {
                'name': 'Stage Lighting',
                'slug': 'stage-lighting',
                'icon': 'fas fa-lightbulb',
                'tagline': 'Create Atmosphere and Drama',
                'image': 'images/stage-lighting.jpg',
                'image_large': 'images/stage-lighting.jpg',
                'full_description': 'Lighting transforms ordinary spaces into extraordinary experiences. At BluePrint AV, we design and execute sophisticated lighting schemes that enhance performances, set moods, and guide audience attention. Our comprehensive lighting inventory includes moving heads, wash lights, beam fixtures, LED pars, blinders, strobes, and atmospheric effects like haze and fog machines.\n\nOur certified lighting designers work closely with you to understand your creative vision and technical requirements. We create detailed lighting plots and cue sequences using industry-standard software like grandMA2/3, Hog, and Chamsys. Whether you need subtle architectural lighting for a corporate gala or an energetic light show for a concert, our team delivers spectacular results.\n\nWe also provide custom color mixing, gobo projection, and pixel mapping capabilities that allow us to create truly unique visual experiences. Our on-site lighting directors manage every aspect of your show, from pre-programming to live operation.',
                'features': [
                    'Moving Head Lights',
                    'Wash & Beam Lights',
                    'Laser Effects',
                    'DMX Control Systems',
                    'Custom Cue Programming',
                    'Haze/Fog Atmospheric Effects'
                ],
                'technologies': ['Martin', 'Clay Paky', 'GLP', 'grandMA', 'Chamsys', 'ADJ'],
                'industries': ['Concerts', 'Weddings', 'Corporate Galas', 'Clubs', 'Theatre', 'Fashion Shows'],
                'experience_years': 11,
                'projects_completed': 520,
                'happy_clients': 460
            },
            {
                'name': 'Event Production',
                'slug': 'event-production',
                'icon': 'fas fa-cogs',
                'tagline': 'From Concept to Curtain Call',
                'image': 'images/event-production.jpg',
                'image_large': 'images/event-production.jpg',
                'full_description': 'BluePrint AV offers end-to-end event production services that take your vision from concept to reality. Our experienced production managers coordinate every technical aspect of your event, including audio, lighting, video, staging, rigging, and power distribution. We serve as your single point of contact, eliminating the stress of managing multiple vendors.\n\nOur pre-production process includes site visits, technical drawings, equipment planning, and load-in scheduling. We create detailed production schedules that ensure every element comes together seamlessly on show day. Our inventory includes staging systems, truss structures, risers, drapery, and scenic elements that can be customized to match your event\'s aesthetic.\n\nDuring your event, our technical directors manage all production elements, coordinating with your speakers, performers, and venue staff. We provide backup systems and redundant configurations for critical events, ensuring reliability even in unexpected situations.',
                'features': [
                    'Stage Design & Construction',
                    'Technical Direction',
                    'On-site Coordination',
                    'Equipment Logistics',
                    'Rigging & Truss Systems',
                    'Power Distribution'
                ],
                'technologies': ['Global Truss', 'Tomcat', 'Litec', 'StageLine', 'Chain Hoists', 'Generator Systems'],
                'industries': ['Festivals', 'Corporate Events', 'Concerts', 'Award Ceremonies', 'Conferences', 'Private Events'],
                'experience_years': 10,
                'projects_completed': 280,
                'happy_clients': 250
            },
            {
                'name': 'DJ & Entertainment',
                'slug': 'dj-entertainment',
                'icon': 'fas fa-headphones-alt',
                'tagline': 'Keep Your Guests Dancing All Night',
                'image': 'images/dj-entertainment.jpg',
                'image_large': 'images/dj-entertainment.jpg',
                'full_description': 'Create unforgettable moments with BluePrint AV\'s professional DJ and entertainment services. Our roster includes experienced DJs who specialize in every genre, from Top 40 and house to Afrobeat, Amapiano, and corporate background music. We work closely with you to understand your musical preferences and curate playlists that match your event\'s energy and atmosphere.\n\nOur DJs use professional-grade equipment including Pioneer CDJ/XDJ systems, Allen & Heath mixers, and high-output sound systems. We provide options for MC services, live percussionists, saxophonists, and vocalists who can perform alongside our DJs to elevate the experience.\n\nWe also offer complete entertainment packages that include lighting effects, CO2 cannons, confetti blasts, and sparkular machines for high-energy moments. From weddings and private parties to corporate events and club nights, our entertainment team delivers exceptional experiences.',
                'features': [
                    'Professional DJs',
                    'Curated Playlists',
                    'MC & Host Services',
                    'Live Musicians Available',
                    'Special Effects (CO2, Confetti)',
                    'Uplighting Packages'
                ],
                'technologies': ['Pioneer CDJ/XDJ', 'Allen & Heath', 'Rane', 'Serato', 'Rekordbox', 'Traktor'],
                'industries': ['Weddings', 'Private Parties', 'Corporate Events', 'Clubs', 'Festivals', 'Birthdays'],
                'experience_years': 8,
                'projects_completed': 680,
                'happy_clients': 650
            },
            {
                'name': 'Live Streaming',
                'slug': 'live-streaming',
                'icon': 'fas fa-video',
                'tagline': 'Reach Audiences Anywhere in the World',
                'image': 'images/live-streaming.jpg',
                'image_large': 'images/live-streaming.jpg',
                'full_description': 'Extend your event\'s reach beyond physical limitations with BluePrint AV\'s professional live streaming services. We provide complete hybrid event solutions that seamlessly integrate in-person and virtual audiences. Our streaming packages include multi-camera production, professional encoding, and delivery to platforms including YouTube, Vimeo, Zoom, Teams, and custom RTMP destinations.\n\nOur production team uses broadcast-quality cameras, switchers, and audio interfaces to deliver polished streams that look and sound professional. We provide graphics overlays, lower thirds, and branded elements that reinforce your event\'s identity. For interactive events, we integrate live chat, Q&A moderation, and polling features that keep remote attendees engaged.\n\nWe also offer recording services that capture your event for on-demand viewing, training materials, or promotional content. Our cloud recording solutions provide secure storage and easy sharing options.',
                'features': [
                    'Multi-camera Production',
                    'Platform Integration',
                    'Hybrid Event Solutions',
                    'Cloud Recording',
                    'Graphics Overlays',
                    'Audience Engagement Tools'
                ],
                'technologies': ['Blackmagic', 'vMix', 'OBS', 'StreamYard', 'Zoom', 'YouTube Live'],
                'industries': ['Conferences', 'Webinars', 'Hybrid Events', 'Virtual Summits', 'Live Performances', 'Corporate Meetings'],
                'experience_years': 6,
                'projects_completed': 180,
                'happy_clients': 170
            },
            {
                'name': 'Conference AV',
                'slug': 'conference-av',
                'icon': 'fas fa-chalkboard',
                'tagline': 'Flawless Presentations and Collaboration',
                'image': 'images/conference-av.jpg',
                'image_large': 'images/conference-av.jpg',
                'full_description': 'Deliver impactful conferences and corporate events with BluePrint AV\'s specialized audiovisual solutions. We understand the unique requirements of professional gatherings, including multiple breakout sessions, keynote presentations, panel discussions, and networking sessions. Our conference packages include wireless microphones, audience response systems, presentation switching, and recording capabilities.\n\nOur inventory includes gooseneck microphones, boundary mics, handheld wireless systems, and lapel mics suitable for any speaker configuration. We provide confidence monitors, IMAG displays, and large-format projection systems that ensure all attendees have clear sightlines to presentation content. For multilingual events, we offer interpretation systems including IR receivers, headsets, and interpreter booths.\n\nOur technical team manages every aspect of your conference, from speaker rehearsals to session transitions. We provide clickers for presenters, slide advancers, and dedicated presentation laptops configured for seamless playback.',
                'features': [
                    'Conference Microphones',
                    'Translation Systems',
                    'Presentation Switching',
                    'Recording & Playback',
                    'Audience Response Systems',
                    'Speaker Support Equipment'
                ],
                'technologies': ['Shure', 'Sennheiser', 'Crestron', 'Extron', 'Barco', 'Kramer'],
                'industries': ['Corporate Conferences', 'Academic Events', 'Government Meetings', 'Medical Conferences', 'Board Meetings', 'Training Sessions'],
                'experience_years': 9,
                'projects_completed': 350,
                'happy_clients': 330
            },
            {
                'name': 'Set Design',
                'slug': 'set-design',
                'icon': 'fas fa-paintbrush',
                'tagline': 'Transform Your Venue into an Experience',
                'image': 'images/set-design.jpg',
                'image_large': 'images/set-design.jpg',
                'full_description': 'Create immersive environments that captivate your audience with BluePrint AV\'s custom set design and fabrication services. Our creative team collaborates with you to develop concepts that bring your brand or event theme to life through physical structures, scenic elements, and integrated technology. We handle everything from initial sketches to final installation, ensuring your vision becomes reality.\n\nOur fabrication shop produces custom staging, risers, podiums, backdrops, and scenic elements using materials including wood, metal, acrylic, and fabric. We incorporate LED video panels, projection surfaces, and lighting fixtures directly into set pieces for integrated designs that maximize visual impact. Our inventory includes modular staging systems that can be configured for any venue size or layout.\n\nFor branded environments, we produce custom signage, step-and-repeats, photo walls, and product display units that reinforce your messaging. Our installation crews work efficiently to transform venues while respecting load-in windows and venue requirements.',
                'features': [
                    'Custom Fabrication',
                    'Scenic Design',
                    'Branded Environments',
                    'Prop & Decor Rental',
                    'Modular Staging',
                    'Photo Walls & Backdrops'
                ],
                'technologies': ['CAD Design', 'CNC Routing', 'Laser Cutting', '3D Modeling', 'Scenic Painting', 'LED Integration'],
                'industries': ['Corporate Events', 'Product Launches', 'Weddings', 'Photo Shoots', 'TV Production', 'Experiential Marketing'],
                'experience_years': 8,
                'projects_completed': 150,
                'happy_clients': 140
            }
        ]
        return context
    
class ServiceDetailView(TemplateView):
    template_name = 'Home/service_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get('slug')
        
        # Get the home view to access services data
        home_view = HomeView()
        services = home_view.get_context_data()['services']
        
        # Find the requested service
        service = next((s for s in services if s['slug'] == slug), None)
        context['service'] = service
        
        # Get related services (excluding current)
        context['related_services'] = [s for s in services if s['slug'] != slug][:3]
        
        return context

class QuoteCreateView(CreateView):
    model = Quote
    form_class = QuoteModelForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(
            self.request, 
            "Thank you! We'll get back to you within 24 hours."
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(
            self.request, 
            "Please correct the errors below and try again."
        )
        return super().form_invalid(form)