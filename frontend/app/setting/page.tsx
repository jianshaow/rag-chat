import { SettingProvider } from '@/context/setting-context';
import Link from 'next/link';
import '../styles/common.css';
import AppConfigSetting from './components/AppConfig';
import GeneralConfigSetting from './components/GeneralConfig';
import ModelConfigSetting from './components/ModelConfig';
import './Setting.css';

export default function Page() {
  return (
    <div className='main-frame'>
      <div className='header'>
        <Link href='/query'>Return Home</Link>
      </div>
      <h1 className='title'>Settings</h1>
      <SettingProvider>
        <GeneralConfigSetting />
        <AppConfigSetting />
        <ModelConfigSetting />
      </SettingProvider>
    </div>
  )
}