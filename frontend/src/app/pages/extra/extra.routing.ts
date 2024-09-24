import { Routes } from '@angular/router';


// pages
import {AppImportacaoComponent} from "./importacao/importacao.component";
import {AppParametrosComponent} from "./parametros/parametros.component";

export const ExtraRoutes: Routes = [
  {
    path: '',
    children: [
      {
        path: 'importacao',
        component: AppImportacaoComponent,
      },
      {
        path: 'parametros',
        component: AppParametrosComponent,
      },
    ],
  },
];
