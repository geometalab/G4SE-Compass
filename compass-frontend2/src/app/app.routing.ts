import { Routes, RouterModule } from '@angular/router';
import {MetadataComponent} from "./metadata/metadata.component";


const appRoutes: Routes = [
  {
    path: '',
    redirectTo: '/metadata',
    pathMatch: 'full'
  },
  // {
  //   path: 'detail/:id',
  //   component: HeroDetailComponent
  // },
  {
    path: 'metadata',
    component: MetadataComponent
  }
];

export const routing = RouterModule.forRoot(appRoutes);

export const routedComponents = [MetadataComponent];
