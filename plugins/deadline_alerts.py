import asyncio

from airflow.providers.smtp.hooks.smtp import SmtpHook


def _field(obj, name):
    return obj[name] if isinstance(obj, dict) else getattr(obj, name)


async def send_deadline_email(context, to, subject="[airflow] Deadline missed: {dag_id}", html_content=None, conn_id="smtp_default"):
    dag_run = context["dag_run"]
    dag_id = _field(dag_run, "dag_id")
    run_id = _field(dag_run, "run_id" if _has(dag_run, "run_id") else "dag_run_id")
    body = (html_content or "Run <b>{run_id}</b> of <b>{dag_id}</b> did not finish within its deadline.").format(
        dag_id=dag_id, run_id=run_id
    )

    def _send():
        with SmtpHook(smtp_conn_id=conn_id) as hook:
            hook.send_email_smtp(to=to, subject=subject.format(dag_id=dag_id, run_id=run_id), html_content=body)

    await asyncio.to_thread(_send)


def _has(obj, name):
    return name in obj if isinstance(obj, dict) else hasattr(obj, name)
