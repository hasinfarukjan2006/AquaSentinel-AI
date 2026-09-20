import React, { useEffect, useState } from 'react';
import { Cpu, AlertCircle, CheckCircle2, ShieldAlert } from 'lucide-react';
import { fetchModelStatus } from '../services/api';

export default function ModelStatusPage() {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    async function loadStatus() {
      try {
        const res = await fetchModelStatus();
        setStatus(res);
      } catch (err) {
        console.error("Error fetching model status:", err);
      }
    }
    loadStatus();
  }, []);

  if (!status) return null;

  const demoEval = status.evaluation?.Synthetic_Demo_Dataset_Evaluation;
  const realEval = status.evaluation?.Real_Public_Source_Evaluation;

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-slate-900 text-white p-5 rounded-xl border border-slate-800 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold flex items-center space-x-2">
            <Cpu className="w-6 h-6 text-blue-400" />
            <span>ML Model Status & Performance Audit</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Machine Learning Pipeline Architecture: Random Forest, Logistic Regression Baseline, Isolation Forest
          </p>
        </div>
        <span className="text-xs bg-emerald-900 text-emerald-300 border border-emerald-700 px-3 py-1 rounded font-mono font-bold">
          Model: {status.model_status}
        </span>
      </div>

      {/* Model vs Real World Event Clarification Banner */}
      <div className="bg-amber-50 border border-amber-200 p-4 rounded-xl flex items-start space-x-3 text-amber-900 text-xs">
        <AlertCircle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <span className="font-bold text-slate-900">Critical Model Distinction Requirement:</span>
          <p className="text-amber-800 leading-relaxed">
            "The system clearly distinguishes <strong>MODEL OUTPUT</strong> from a <strong>REAL-WORLD CONFIRMED EVENT</strong>. Machine learning outputs are statistical risk signals designed to support decision-making, NOT automatic outbreak declarations."
          </p>
        </div>
      </div>

      {/* Supervised Metrics Cards (Synthetic Demo Dataset) */}
      {demoEval && (
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
          <div className="flex items-center justify-between border-b pb-3">
            <div>
              <h2 className="text-base font-bold text-slate-900">Synthetic Demo Dataset Supervised Performance</h2>
              <p className="text-xs text-slate-500">Evaluated on {demoEval.sample_count} multi-indicator records</p>
            </div>
            <span className="text-xs font-mono bg-blue-50 text-blue-700 border border-blue-200 px-2.5 py-1 rounded">
              Supervised Validation
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Random Forest Classifier */}
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 space-y-3">
              <div className="font-bold text-sm text-slate-900 flex items-center justify-between">
                <span>Random Forest Prototype Classifier</span>
                <span className="text-xs text-blue-600 font-mono">Main Prototype</span>
              </div>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="bg-white p-2.5 rounded border border-slate-200">
                  <span className="text-slate-500 block">Precision</span>
                  <span className="text-base font-bold text-slate-900">{demoEval.random_forest.precision * 100}%</span>
                </div>
                <div className="bg-white p-2.5 rounded border border-slate-200">
                  <span className="text-slate-500 block">Recall</span>
                  <span className="text-base font-bold text-slate-900">{demoEval.random_forest.recall * 100}%</span>
                </div>
                <div className="bg-white p-2.5 rounded border border-slate-200">
                  <span className="text-slate-500 block">F1 Score</span>
                  <span className="text-base font-bold text-slate-900">{demoEval.random_forest.f1_score}</span>
                </div>
                <div className="bg-white p-2.5 rounded border border-slate-200">
                  <span className="text-slate-500 block">ROC-AUC</span>
                  <span className="text-base font-bold text-slate-900">{demoEval.random_forest.roc_auc}</span>
                </div>
              </div>
            </div>

            {/* Logistic Regression Baseline */}
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 space-y-3">
              <div className="font-bold text-sm text-slate-900 flex items-center justify-between">
                <span>Logistic Regression</span>
                <span className="text-xs text-slate-500 font-mono">Baseline Model</span>
              </div>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="bg-white p-2.5 rounded border border-slate-200">
                  <span className="text-slate-500 block">Precision</span>
                  <span className="text-base font-bold text-slate-900">{demoEval.logistic_regression.precision * 100}%</span>
                </div>
                <div className="bg-white p-2.5 rounded border border-slate-200">
                  <span className="text-slate-500 block">Recall</span>
                  <span className="text-base font-bold text-slate-900">{demoEval.logistic_regression.recall * 100}%</span>
                </div>
                <div className="bg-white p-2.5 rounded border border-slate-200">
                  <span className="text-slate-500 block">F1 Score</span>
                  <span className="text-base font-bold text-slate-900">{demoEval.logistic_regression.f1_score}</span>
                </div>
                <div className="bg-white p-2.5 rounded border border-slate-200">
                  <span className="text-slate-500 block">ROC-AUC</span>
                  <span className="text-base font-bold text-slate-900">{demoEval.logistic_regression.roc_auc}</span>
                </div>
              </div>
            </div>

          </div>
        </div>
      )}

      {/* Real Dataset Honest Evaluation Notice */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-3">
        <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
          <ShieldAlert className="w-5 h-5 text-blue-600" />
          <span>Real Public Source Dataset Evaluation Status</span>
        </h2>
        <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-2 text-xs">
          <div className="font-bold text-slate-900 text-sm text-rose-700">
            "{realEval?.status_message || 'Insufficient labelled data for reliable supervised model evaluation.'}"
          </div>
          <p className="text-slate-600 leading-relaxed">
            {realEval?.explanation || 'Real public health data provides national summary figures without confirmed epidemic labels per district.'}
          </p>
        </div>
      </div>

      {/* Features Used List */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-3">
        <h2 className="text-base font-bold text-slate-900">Features Consumed by Model Pipeline</h2>
        <div className="flex flex-wrap gap-2 text-xs">
          {(status.features_used || []).map((feat, i) => (
            <span key={i} className="bg-slate-100 text-slate-800 border border-slate-300 font-mono px-2.5 py-1 rounded">
              {feat}
            </span>
          ))}
        </div>
      </div>

    </div>
  );
}
