import { Injectable } from '@angular/core';
import { Headers, Http, Response } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import {Metadata} from "./metadata";
import {MetadataParameters} from "./metadata-parameters";

@Injectable()
export class MetadataService {
  private metadataUrl = 'api/metadata/';  // URL to web API

  constructor(private http: Http) { }

  getMetadataList(params: MetadataParameters=undefined): Promise<Metadata[]> {
    if (params == undefined) {
      params = new MetadataParameters();
    }
    var urlParams = params.toUrlQuery();
    return this.http
      .get(this.metadataUrl + urlParams)
      .toPromise()
      .then(response => response.json() as any[])
      .catch(this.handleError);
  }
  private handleError(error: any): Promise<Metadata> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
