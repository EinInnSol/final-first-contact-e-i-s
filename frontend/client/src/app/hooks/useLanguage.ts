'use client';

import { useState, useEffect, useCallback } from 'react';

export type Language = 'en' | 'es' | 'km' | 'tl' | 'ko';

interface LanguageConfig {
  name: string;
  direction: 'ltr' | 'rtl';
  flag: string;
}

const LANGUAGES: Record<Language, LanguageConfig> = {
  en: { name: 'English', direction: 'ltr', flag: '🇺🇸' },
  es: { name: 'Español', direction: 'ltr', flag: '🇪🇸' },
  km: { name: 'ខ្មែរ', direction: 'ltr', flag: '🇰🇭' },
  tl: { name: 'Tagalog', direction: 'ltr', flag: '🇵🇭' },
  ko: { name: '한국어', direction: 'ltr', flag: '🇰🇷' },
};

// Translation keys - in a real app, these would be loaded from external files
const translations: Record<Language, Record<string, string>> = {
  en: {
    'welcome.title': 'Welcome to First Contact EIS',
    'welcome.subtitle': 'Your gateway to comprehensive social services in Long Beach',
    'welcome.get_started': 'Get Started',
    'features.housing.title': 'Housing Assistance',
    'features.housing.description': 'Emergency shelter, transitional housing, and permanent housing solutions',
    'features.employment.title': 'Employment Services',
    'features.employment.description': 'Job training, resume building, and career development programs',
    'features.healthcare.title': 'Healthcare Access',
    'features.healthcare.description': 'Medical care, mental health services, and wellness programs',
    'dashboard.title': 'Client Portal',
    'dashboard.welcome_back': 'Welcome back',
    'tabs.ai_chat': 'AI Chat',
    'tabs.my_cases': 'My Cases',
    'tabs.service_requests': 'Service Requests',
    'tabs.resources': 'Resources',
    'tabs.profile': 'Profile',
    'tabs.settings': 'Settings',
    'crisis.alert_detected': 'Crisis situation detected. Please seek immediate help.',
    'crisis.resolved': 'Crisis situation resolved.',
    'notifications.new_notification': 'New notification received',
    'cases.updated': 'Case updated',
    'settings.title': 'Settings',
    'settings.coming_soon': 'Settings panel coming soon',
  },
  es: {
    'welcome.title': 'Bienvenido a First Contact EIS',
    'welcome.subtitle': 'Su puerta de entrada a servicios sociales integrales en Long Beach',
    'welcome.get_started': 'Comenzar',
    'features.housing.title': 'Asistencia de Vivienda',
    'features.housing.description': 'Refugio de emergencia, vivienda transitoria y soluciones de vivienda permanente',
    'features.employment.title': 'Servicios de Empleo',
    'features.employment.description': 'Capacitación laboral, construcción de currículum y programas de desarrollo profesional',
    'features.healthcare.title': 'Acceso a la Atención Médica',
    'features.healthcare.description': 'Atención médica, servicios de salud mental y programas de bienestar',
    'dashboard.title': 'Portal del Cliente',
    'dashboard.welcome_back': 'Bienvenido de nuevo',
    'tabs.ai_chat': 'Chat IA',
    'tabs.my_cases': 'Mis Casos',
    'tabs.service_requests': 'Solicitudes de Servicio',
    'tabs.resources': 'Recursos',
    'tabs.profile': 'Perfil',
    'tabs.settings': 'Configuración',
    'crisis.alert_detected': 'Situación de crisis detectada. Busque ayuda inmediata.',
    'crisis.resolved': 'Situación de crisis resuelta.',
    'notifications.new_notification': 'Nueva notificación recibida',
    'cases.updated': 'Caso actualizado',
    'settings.title': 'Configuración',
    'settings.coming_soon': 'Panel de configuración próximamente',
  },
  km: {
    'welcome.title': 'សូមស្វាគមន៍មកកាន់ First Contact EIS',
    'welcome.subtitle': 'ច្រកចូលរបស់អ្នកទៅកាន់សេវាកម្មសង្គមទូលំទូលាយនៅ Long Beach',
    'welcome.get_started': 'ចាប់ផ្តើម',
    'features.housing.title': 'ជំនួយផ្ទះសម្បែង',
    'features.housing.description': 'ទីជម្រកបន្ទាន់ ផ្ទះសម្បែងចម្លង និងដំណោះស្រាយផ្ទះសម្បែងអចិន្ត្រៃយ៍',
    'features.employment.title': 'សេវាកម្មការងារ',
    'features.employment.description': 'ការបណ្តុះបណ្តាលការងារ ការបង្កើតប្រវត្តិរូប និងកម្មវិធីអភិវឌ្ឍន៍អាជីព',
    'features.healthcare.title': 'ការចូលប្រើសេវាកម្មសុខភាព',
    'features.healthcare.description': 'ការថែទាំវេជ្ជសាស្ត្រ សេវាកម្មសុខភាពចិត្ត និងកម្មវិធីសុខភាព',
    'dashboard.title': 'ផ្ទៃតាប្លូអតិថិជន',
    'dashboard.welcome_back': 'សូមស្វាគមន៍មកវិញ',
    'tabs.ai_chat': 'ជជែក AI',
    'tabs.my_cases': 'ករណីរបស់ខ្ញុំ',
    'tabs.service_requests': 'សំណើសេវាកម្ម',
    'tabs.resources': 'ធនធាន',
    'tabs.profile': 'ប្រវត្តិរូប',
    'tabs.settings': 'ការកំណត់',
    'crisis.alert_detected': 'បានរកឃើញស្ថានការណ៍វិបត្តិ។ សូមស្វែងរកជំនួយភ្លាមៗ។',
    'crisis.resolved': 'ស្ថានការណ៍វិបត្តិត្រូវបានដោះស្រាយ។',
    'notifications.new_notification': 'បានទទួលការជូនដំណឹងថ្មី',
    'cases.updated': 'ករណីត្រូវបានធ្វើបច្ចុប្បន្នភាព',
    'settings.title': 'ការកំណត់',
    'settings.coming_soon': 'បន្ទះការកំណត់នឹងមកដល់ឆាប់ៗនេះ',
  },
  tl: {
    'welcome.title': 'Maligayang pagdating sa First Contact EIS',
    'welcome.subtitle': 'Ang inyong gateway sa komprehensibong serbisyong panlipunan sa Long Beach',
    'welcome.get_started': 'Magsimula',
    'features.housing.title': 'Tulong sa Pabahay',
    'features.housing.description': 'Emergency shelter, transitional housing, at permanenteng solusyon sa pabahay',
    'features.employment.title': 'Serbisyong Pang-employment',
    'features.employment.description': 'Job training, resume building, at career development programs',
    'features.healthcare.title': 'Access sa Healthcare',
    'features.healthcare.description': 'Medical care, mental health services, at wellness programs',
    'dashboard.title': 'Client Portal',
    'dashboard.welcome_back': 'Maligayang pagbabalik',
    'tabs.ai_chat': 'AI Chat',
    'tabs.my_cases': 'Aking mga Kaso',
    'tabs.service_requests': 'Service Requests',
    'tabs.resources': 'Mga Resources',
    'tabs.profile': 'Profile',
    'tabs.settings': 'Settings',
    'crisis.alert_detected': 'Nadetect ang crisis situation. Mangyaring humingi ng agarang tulong.',
    'crisis.resolved': 'Naresolba ang crisis situation.',
    'notifications.new_notification': 'Nakatanggap ng bagong notification',
    'cases.updated': 'Na-update ang kaso',
    'settings.title': 'Settings',
    'settings.coming_soon': 'Settings panel ay darating na',
  },
  ko: {
    'welcome.title': 'First Contact EIS에 오신 것을 환영합니다',
    'welcome.subtitle': '롱비치의 포괄적인 사회 서비스로의 관문',
    'welcome.get_started': '시작하기',
    'features.housing.title': '주거 지원',
    'features.housing.description': '긴급 대피소, 전환 주거, 영구 주거 솔루션',
    'features.employment.title': '고용 서비스',
    'features.employment.description': '직업 훈련, 이력서 작성, 경력 개발 프로그램',
    'features.healthcare.title': '의료 서비스 접근',
    'features.healthcare.description': '의료 서비스, 정신 건강 서비스, 웰니스 프로그램',
    'dashboard.title': '클라이언트 포털',
    'dashboard.welcome_back': '다시 오신 것을 환영합니다',
    'tabs.ai_chat': 'AI 채팅',
    'tabs.my_cases': '내 사례',
    'tabs.service_requests': '서비스 요청',
    'tabs.resources': '자원',
    'tabs.profile': '프로필',
    'tabs.settings': '설정',
    'crisis.alert_detected': '위기 상황이 감지되었습니다. 즉시 도움을 요청하세요.',
    'crisis.resolved': '위기 상황이 해결되었습니다.',
    'notifications.new_notification': '새 알림을 받았습니다',
    'cases.updated': '사례가 업데이트되었습니다',
    'settings.title': '설정',
    'settings.coming_soon': '설정 패널이 곧 제공됩니다',
  },
};

export function useLanguage() {
  const [language, setLanguageState] = useState<Language>('en');

  // Load language from localStorage on mount
  useEffect(() => {
    const savedLanguage = localStorage.getItem('language') as Language;
    if (savedLanguage && LANGUAGES[savedLanguage]) {
      setLanguageState(savedLanguage);
    }
  }, []);

  // Save language to localStorage when changed
  const setLanguage = useCallback((newLanguage: Language) => {
    setLanguageState(newLanguage);
    localStorage.setItem('language', newLanguage);
    
    // Update document direction
    document.documentElement.dir = LANGUAGES[newLanguage].direction;
    document.documentElement.lang = newLanguage;
  }, []);

  // Translation function
  const t = useCallback((key: string): string => {
    return translations[language]?.[key] || translations.en[key] || key;
  }, [language]);

  // Get current language config
  const getLanguageConfig = useCallback(() => {
    return LANGUAGES[language];
  }, [language]);

  // Get all available languages
  const getAvailableLanguages = useCallback(() => {
    return Object.entries(LANGUAGES).map(([code, config]) => ({
      code: code as Language,
      ...config,
    }));
  }, []);

  return {
    language,
    setLanguage,
    t,
    getLanguageConfig,
    getAvailableLanguages,
  };
}
