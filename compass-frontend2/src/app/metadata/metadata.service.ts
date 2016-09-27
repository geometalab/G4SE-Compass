import { Injectable } from '@angular/core';
import { Headers, Http, Response } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import {Metadata} from "./metadata";

@Injectable()
export class MetadataService {
  private metadataUrl = 'api/metadata';  // URL to web API

  constructor(private http: Http) { }

  getMetadataList(): Promise<Metadata[]> {
    return this.http
      .get(this.metadataUrl)
      .toPromise()
      .then(response => response.json().results as any[])
      .catch(this.handleError);
  }
  private handleError(error: any): Promise<Metadata> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
