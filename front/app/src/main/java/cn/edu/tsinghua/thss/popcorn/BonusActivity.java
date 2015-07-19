package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.view.annotation.ViewInject;
import com.lidroid.xutils.view.annotation.event.OnClick;


public class BonusActivity extends Activity {
    ProgressDialog progressDialog;

    @ViewInject(R.id.id_lottery_result)
    private TextView mTextViewResult;

    @ViewInject(R.id.id_get_lottery_btn)
    private Button mButtonGetLottery;

    @OnClick(R.id.id_get_lottery_btn)
    private void getLotteryButtonClick(View v) {
        progressDialog.show();

        new Thread(new Runnable() {

            @Override
            public void run() {
                // TODO Auto-generated method stub
                try {
                    Thread.sleep(1000);
                    progressDialog.cancel();
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

            }
        }).start();
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bonus);
        ViewUtils.inject(this);

        progressDialog = new ProgressDialog(BonusActivity.this, R.style.buffer_dialog);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setMessage("请稍候...");
        progressDialog.setIndeterminate(false);
        progressDialog.setCancelable(false);
        progressDialog.setOnCancelListener(new DialogInterface.OnCancelListener() {
            @Override
            public void onCancel(DialogInterface dialog) {
                mTextViewResult.setText("很遗憾，您没有中奖，下次再来！");
                mButtonGetLottery.setVisibility(View.GONE);
            }
        });
    }

    @Override
    protected  void onDestroy(){
        progressDialog.dismiss();
        super.onDestroy();
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.bonus, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            BonusActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
