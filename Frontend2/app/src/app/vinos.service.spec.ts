import { TestBed } from '@angular/core/testing';

import { VinosService } from './vinos.service';

describe('VinosService', () => {
  let service: VinosService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VinosService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
