import { Routes, RouterModule } from '@angular/router';
import {MetadataComponent} from "./metadata/metadata.component";
import {MetadataDetailComponent} from "./metadata/metadata-detail.component";
import {SearchComponent} from "./metadata/search/search.component";


const appRoutes: Routes = [
  {
    path: '',
    redirectTo: '/search',
    pathMatch: 'full'
  },
  // {
  //   path: 'detail/:id',
  //   component: HeroDetailComponent
  // },
  {
    path: 'metadata',
    component: MetadataComponent
  },
  {
    path: 'metadata/:id',
    component: MetadataDetailComponent
  },
  {
    path: 'search',
    component: SearchComponent
  },
];

export const routing = RouterModule.forRoot(appRoutes);

export const routedComponents = [MetadataComponent];
