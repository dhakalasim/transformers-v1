import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { BotInfo } from './transformer.model';
import { TransformerService } from './transformer.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  bots: BotInfo[] = [];
  formats: string[] = [];

  content = '{\n  "faction": "Autobots",\n  "leader": "Optimus Prime"\n}';
  fromFormat = 'json';
  toFormat = 'yaml';

  result = '';
  botUsed = '';
  error = '';
  loading = false;

  constructor(private transformerService: TransformerService) {}

  ngOnInit(): void {
    this.transformerService.listBots().subscribe({
      next: (bots) => {
        this.bots = bots;
        const formatSet = new Set<string>();
        bots.forEach((bot) =>
          bot.conversions.forEach(([from, to]) => {
            formatSet.add(from);
            formatSet.add(to);
          })
        );
        this.formats = Array.from(formatSet).sort();
      },
      error: () => {
        this.error = 'Could not reach the Autobot fleet. Is the backend running?';
      }
    });
  }

  rollOut(): void {
    this.result = '';
    this.botUsed = '';
    this.error = '';
    this.loading = true;

    this.transformerService
      .transform({
        content: this.content,
        from_format: this.fromFormat,
        to_format: this.toFormat
      })
      .subscribe({
        next: (response) => {
          this.result = response.result;
          this.botUsed = response.bot_name;
          this.loading = false;
        },
        error: (err: HttpErrorResponse) => {
          this.error = err.error?.detail ?? 'Transformation failed.';
          this.loading = false;
        }
      });
  }
}
