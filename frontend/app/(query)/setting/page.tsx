import Link from 'next/link';
import '../query.module.css';
import AppConfigSetting from './components/AppConfig';
import GeneralConfigSetting from './components/GeneralConfig';
import ModelConfigSetting from './components/ModelConfig';
import './page.module.css';

export default function Page() {
  return (
    <div className='main-frame'>
      <div className='header'>
        <Link href='/query'>Return Home</Link>
      </div>
      <h1 className='title'>Settings</h1>
      <GeneralConfigSetting />
      <AppConfigSetting />
      <ModelConfigSetting />
    </div>
  )
}