package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.ListActivity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.os.SystemClock;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Timer;
import java.util.TimerTask;

import com.beardedhen.androidbootstrap.FontAwesomeText;
import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.utils.NoRepeatToast;

public class RepairListActivity extends ListActivity {
    JSONArray repairTaskList = null;
    ProgressDialog progressDialog;
    static private int REQUEST_CODE = 2;
    RepairTaskListAdapter adapter;

    Handler handler = new Handler() {
        public void handleMessage(Message msg) {
            getRepairTaskList();
            super.handleMessage(msg);
        };
    };
    Timer timer = new Timer();
    TimerTask task = new TimerTask() {

        @Override
        public void run() {
            // 需要做的事:发送消息
            Message message = new Message();
            message.what = 1;
            handler.sendMessage(message);
        }
    };

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //progressDialog = new ProgressDialog(RepairListActivity.this, R.style.buffer_dialog);
        //progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        //progressDialog.setMessage("数据加载中...");
       // progressDialog.setIndeterminate(false);
        //progressDialog.setCancelable(false);
       // progressDialog.show();
        getRepairTaskList();
        //timer.schedule(task, Config.REPAIR_UPDATE_DELAY, Config.REPAIR_UPDATE_INTERVAL); // 1s后执行task,经过2s再次执行
//        SystemClock.sleep(3000);//睡3秒
        //progressDialog.hide();
    }

    private void getRepairTaskList(){

        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.REPAIR_TASK_LIST_URL,
                params,
                new RequestCallBack<String>() {
                    @Override
                    public void onStart() {
                    }

                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }

                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try {
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");
                            if (status.equals("ok")) {
                                repairTaskList = jsonObject.getJSONArray("data");
                                adapter = new RepairTaskListAdapter(RepairListActivity.this);
                                setListAdapter(adapter);
                            } else {
                                //Toast.makeText(getApplicationContext(), "服务器内部出错", Toast.LENGTH_SHORT).show();
                                NoRepeatToast.showToast(getApplicationContext(), "服务器内部出错！", Toast.LENGTH_SHORT);
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        //progressDialog.hide();
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        //progressDialog.hide();
                        //Toast.makeText(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT).show();
                        NoRepeatToast.showToast(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT);
                    }
                });
    }

    @Override
    public void onListItemClick(ListView l, View v, int position, long id) {
        Intent intent = new Intent(this, RepairActivity.class);
        Bundle bundle = new Bundle();
        JSONObject task = null;
        try {
            task = repairTaskList.getJSONObject(position);
            bundle.putString("task", task.toString());
            bundle.putInt("position", position);
            intent.putExtras(bundle);
            startActivityForResult(intent, REQUEST_CODE);
        } catch (Exception e) {
            e.printStackTrace();
        }

        super.onListItemClick(l, v, position, id);
    }

    public static JSONArray remove(final int idx, final JSONArray from) {
        final List<JSONObject> objs = asList(from);
        objs.remove(idx);

        final JSONArray ja = new JSONArray();
        for (final JSONObject obj : objs) {
            ja.put(obj);
        }

        return ja;
    }

    public static List<JSONObject> asList(final JSONArray ja) {
        final int len = ja.length();
        final ArrayList<JSONObject> result = new ArrayList<JSONObject>(len);
        for (int i = 0; i < len; i++) {
            final JSONObject obj = ja.optJSONObject(i);
            if (obj != null) {
                result.add(obj);
            }
        }
        return result;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        //比对之前的请求编码，以及核对活动返回的编码是否是Activity.RESULT_OK
        if (Activity.RESULT_OK == resultCode && requestCode == REQUEST_CODE) {
            int position = data.getIntExtra("position", -1);
            boolean isConfirmed = data.getBooleanExtra("isConfirmed", false);
            boolean isUpdated = data.getBooleanExtra("isUpdated", false);
            boolean isSubmitted = data.getBooleanExtra("isSubmitted", false);
            if(isSubmitted){
                try {
                    repairTaskList = remove(position, repairTaskList);
                    setListAdapter(adapter);
                    adapter.notifyDataSetChanged();
                }catch (Exception e){
                    e.printStackTrace();
                }
            }else if(isUpdated){
                String updatedNote = data.getStringExtra("updatedNote");
                try {
                    JSONObject repairTask = repairTaskList.getJSONObject(position);
                    repairTask.put("note", updatedNote);
                    setListAdapter(adapter);
                    adapter.notifyDataSetChanged();
                }catch (Exception e){
                    e.printStackTrace();
                }
            }else if (isConfirmed) {
                try {
                    JSONObject repairTask = repairTaskList.getJSONObject(position);
                    repairTask.put("confirmed", "true");
                    setListAdapter(adapter);
                    adapter.notifyDataSetChanged();
                }catch (Exception e){
                    e.printStackTrace();
                }
            }
        }
    }


    class ViewHolder {
        public TextView title;
        public FontAwesomeText faText;
    }

    public class RepairTaskListAdapter extends BaseAdapter {
        private LayoutInflater mInflater = null;

        public RepairTaskListAdapter(Context context) {
            super();
            mInflater = (LayoutInflater) context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        }

        @Override
        public int getCount() {
            return repairTaskList.length();
        }

        @Override
        public Object getItem(int position) {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public long getItemId(int position) {
            // TODO Auto-generated method stub
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {

            ViewHolder holder = null;
            TextView repairAcceptHint = null;
            if (convertView == null) {
                holder = new ViewHolder();
                convertView = mInflater.inflate(R.layout.listview_repair, null);
                holder.title = (TextView) convertView.findViewById(R.id.title);
                holder.faText = (FontAwesomeText) convertView.findViewById(R.id.front_icon);
                repairAcceptHint = (TextView)convertView.findViewById(R.id.repair_accept_hint);
                convertView.setTag(holder);
            } else {
                holder = (ViewHolder) convertView.getTag();
            }

            try {
                JSONObject repairTask = repairTaskList.getJSONObject(position);
                holder.title.setText(repairTask.getString("title"));

                String repairResult = repairTask.getString("note");
                String confirmed = repairTask.getString("confirmed");
                if(repairResult.length() > 0) {
                    holder.faText.setTextColor(Color.parseColor("#D3D3D3"));
                }else if(confirmed.equals("false")){
                    repairAcceptHint.setVisibility(View.VISIBLE);
                }else{
                    repairAcceptHint.setVisibility(View.GONE);
                }

            } catch (Exception e) {
                e.printStackTrace();
            }

            return convertView;
        }
    }


    @Override
    protected  void onDestroy(){
        //progressDialog.dismiss();
        super.onDestroy();
        //timer.cancel();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.repair_list, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            RepairListActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

}