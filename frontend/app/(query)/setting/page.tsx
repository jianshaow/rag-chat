import Link from 'next/link';
import '../common.css';
import AppConfigSetting from './components/AppConfig';
import GeneralConfigSetting from './components/GeneralConfig';
import ModelConfigSetting from './components/ModelConfig';
import './setting.css';

export default function Page() {
  return (
    <div className='main-frame'>
      <div className='text-right my-2'>
        <Link href='/query'>Return Home</Link>
      </div>
      <h1>Settings</h1>
      <GeneralConfigSetting />
      <AppConfigSetting />
      <ModelConfigSetting />
    </div>
  )
}